Welcome to sphinx-hoverxref!
============================

``sphinx-hoverxref`` is a Sphinx_ extension to add tooltips on the cross references of the documentation with the content of the linked section.

Online documentation:
    https://sphinx-hoverxref.readthedocs.io/

Source code repository (and issue tracker):
    https://github.com/humitos/sphinx-hoverxref/

Badges:
    |Docs badge| |License|


Live example
------------

This is an example of how a ``hoverxref`` link works.
You can include the :ref:`content of another document and section <hoverxref:hoverxref>`.

.. toctree::
   :maxdepth: 1
   :caption: Contents

   installation
   configuration
   development


.. toctree::
   :maxdepth: 1
   :caption: API Reference

   autoapi/hoverxref/index


.. _Sphinx: https://www.sphinx-doc.org/
.. _Read the Docs: https://readthedocs.org


.. |Docs badge| image:: https://readthedocs.org/projects/sphinx-hoverxref/badge/?version=latest
   :target: https://sphinx-hoverxref.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status
.. |License| image:: https://img.shields.io/github/license/humitos/sphinx-hoverxref.svg
   :target: LICENSE
   :alt: Repository license
