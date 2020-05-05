"""
This module is an example of a barebones plugin, using imageio.imread.

It implements the ``napari_get_reader`` hook specification, (to create
a reader plugin) but your plugin may choose to implement any of the hook
specifications offered by napari.

Type annotations here are OPTIONAL!
If you don't care to annotate the return types of your functions
your plugin doesn't need to import, or even depend on napari at all!

Replace code below accordingly.
"""
import numpy as np
import s3fs
import re
import zarr
import requests
import dask.array as da
from vispy.color import Colormap

from pluggy import HookimplMarker

import logging
# DEBUG logging for s3fs so we can track remote calls
logging.basicConfig(level=logging.INFO)
logging.getLogger('s3fs').setLevel(logging.DEBUG)

# for optional type hints only, otherwise you can delete/ignore this stuff
from typing import List, Optional, Union, Any, Tuple, Dict, Callable

LayerData = Union[Tuple[Any], Tuple[Any, Dict], Tuple[Any, Dict, str]]
PathLike = Union[str, List[str]]
ReaderFunction = Callable[[PathLike], List[LayerData]]
# END type hint stuff.

napari_hook_implementation = HookimplMarker("napari")

@napari_hook_implementation
def napari_get_reader(path: PathLike) -> Optional[ReaderFunction]:
    """A basic implementation of the napari_get_reader hook specification."""
    print(' IDR reader ', path)
    if (isinstance(path, str) and path.startswith('https://s3.embassy.ebi.ac.uk/idr/')
            and re.search(r'^.*/(\d+)\.zarr.*', path) is not None):
        return reader_function


def reader_function(path: PathLike) -> List[LayerData]:
    """Take a path or list of paths and return a list of LayerData tuples."""
    print('path', path)
    # path is e.g. https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/6001240.zarr/
    match = re.search(r'^.*/(\d+)\.zarr.*', path)
    image_id = match.group(1)
    return [load_omero_image(image_id)]


def load_omero_image(image_id):

    image_data = requests.get('https://idr.openmicroscopy.org/webclient/imgData/%s/' % image_id).json()
    print(image_data)

    # group '0' is for highest resolution pyramid
    # see https://github.com/ome/omero-ms-zarr/pull/8/files#diff-958e7270f96f5407d7d980f500805b1b
 
    s3 = s3fs.S3FileSystem(
        anon=True,
        client_kwargs={
            'endpoint_url': 'https://s3.embassy.ebi.ac.uk/'
        },
    )
    # top-level
    root_url = 'idr/zarr/v0.1/%s.zarr/' % image_id
    store = s3fs.S3Map(root=root_url, s3=s3, check=False)
    root = zarr.group(store=store)
    root_attrs = root.attrs.asdict()
    # {'multiscales': [{'datasets': [{'path': '0'}, {'path': '1'}], 'version': '0.1'}]}
    print('root_attrs', root.attrs.asdict())

    resolutions = ['0']
    if 'multiscales' in root_attrs:
        resolutions = [d['path'] for d in root_attrs['multiscales'][0]['datasets']]
    print('resolutions', resolutions)

    pyramid = []
    for resolution in resolutions:
        root = 'idr/zarr/v0.1/%s.zarr/%s/' % (image_id, resolution)
        store = s3fs.S3Map(root=root, s3=s3, check=False)
        cached_store = zarr.LRUStoreCache(store, max_size=(2048 * 2**20))
        # data.shape is (t, c, z, y, x) by convention
        data = da.from_zarr(cached_store)
        chunk_sizes = [str(c[0]) + (" (+ %s)" % c[-1] if c[-1] != c[0] else '') for c in data.chunks]
        print('resolution', resolution, 'shape (t, c, z, y, x)', data.shape, 'chunks', chunk_sizes, 'dtype', data.dtype)
        pyramid.append(data)

    colormaps = []
    for ch in image_data['channels']:
        # 'FF0000' -> [1, 0, 0]
        rgb = [(int(ch['color'][i:i+2], 16)/255) for i in range(0, 6, 2)]
        if image_data['rdefs']['model'] == 'greyscale':
            rgb = [1, 1, 1]
        colormaps.append(Colormap([[0, 0, 0], rgb]))
    contrast_limits = [[ch['window']['start'], ch['window']['end']] for ch in image_data['channels']]
    names = [ch['label'] for ch in image_data['channels']]
    visible = [ch['active'] for ch in image_data['channels']]

    return(pyramid, {
        'channel_axis': 1,
        'colormap': colormaps,
        'name': names,
        'contrast_limits': contrast_limits,
        'visible': visible})

    # viewer.dims.set_axis_label(0, 'T')
    # viewer.dims.set_point(0, image_data['rdefs']['defaultT'])
    # viewer.dims.set_axis_label(1, 'Z')
    # viewer.dims.set_point(1, image_data['rdefs']['defaultZ'])
