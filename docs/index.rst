Welcome to sphinx-hoverxref!
============================

``sphinx-hoverxref`` is a Sphinx_ extension to add tooltips on the cross references of the documentation with the content of the linked section. With ``sphinx-hoverxref``, you don’t need to click a link to see what’s in there.

[here goes the image/animation]


Usage
-----

To show a tooltip on a reference, use the role ``hoverxref`` to link to any document or section. This new ``hoverxref`` role is an alias of the ``ref`` role and works in the same.

Simplest usage example:

:header: "Source code", "Output"
:widths: 50, 50

".. code-block:: rst This will :hoverxref:`show a tooltip <hoverxref:hoverxref>` in the linked words."
"This will :hoverxref:`show a tooltip <hoverxref:hoverxref>` in the linked words."


Reference
-----

.. toctree::
   :maxdepth: 1
   :caption: Contents

   installation
   usage
   configuration
   development


Online documentation:
    https://sphinx-hoverxref.readthedocs.io/

Source code repository (and issue tracker):
    https://github.com/readthedocs/sphinx-hoverxref/

Badges:
    |Build| |PyPI version| |Docs badge| |License|
.. toctree::
   :maxdepth: 1
   :caption: API Reference

   autoapi/hoverxref/index


.. _Sphinx: https://www.sphinx-doc.org/
.. _Read the Docs: https://readthedocs.org


.. |Build| image:: https://travis-ci.org/readthedocs/sphinx-hoverxref.svg?branch=master
   :target: https://travis-ci.org/readthedocs/sphinx-hoverxref
   :alt: Build status
.. |PyPI version| image:: https://img.shields.io/pypi/v/sphinx-hoverxref.svg
   :target: https://pypi.org/project/sphinx-hoverxref
   :alt: Current PyPI version
.. |Docs badge| image:: https://readthedocs.org/projects/sphinx-hoverxref/badge/?version=latest
   :target: https://sphinx-hoverxref.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status
.. |License| image:: https://img.shields.io/github/license/readthedocs/sphinx-hoverxref.svg
   :target: LICENSE
   :alt: Repository license
