==========
napari-idr
==========

.. image:: https://img.shields.io/pypi/v/napari-idr.svg
    :target: https://pypi.org/project/napari-idr
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/napari-idr.svg
    :target: https://pypi.org/project/napari-idr
    :alt: Python versions

.. image:: https://travis-ci.org/will-moore/napari-idr.svg?branch=master
    :target: https://travis-ci.org/will-moore/napari-idr
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/will-moore/napari-idr?branch=master
    :target: https://ci.appveyor.com/project/will-moore/napari-idr/branch/master
    :alt: See Build Status on AppVeyor

Open images from idr.openmicroscopy.org

----

This `napari`_ plugin was generated with `Cookiecutter`_ along with `@napari`_'s `cookiecutter-napari-plugin`_ template.


Features
--------

* TODO


Requirements
------------

* TODO


Installation
------------

Install developer mode:

    cd napari-idr
    pip install -e .


Usage
-----

Open images based on their ID in the Image Data Resource.

NB: Only select images are available currently.

For example ID = 9822151 or 6001240.

E.g. to open Image at http://idr.openmicroscopy.org/webclient/?show=image-6001240

```
import napari
with napari.gui_qt():
    viewer = napari.Viewer()
    viewer.open('https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/6001240.zarr/')
```

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
"napari-idr" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@napari`: https://github.com/napari
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`GNU LGPL v3.0`: http://www.gnu.org/licenses/lgpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`Mozilla Public License 2.0`: https://www.mozilla.org/media/MPL/2.0/index.txt
.. _`cookiecutter-napari-plugin`: https://github.com/napari/cookiecutter-napari-plugin
.. _`file an issue`: https://github.com/will-moore/napari-idr/issues
.. _`napari`: https://github.com/napari/napari
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
