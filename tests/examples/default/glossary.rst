Glossary
========

Example page showing the usage of ``.. glossary`` and ``term``.

See definition :term:`builder` for more information.

.. copied from https://www.sphinx-doc.org/en/master/glossary.html

.. glossary::

   builder
      A class (inheriting from :class:`~sphinx.builders.Builder`) that takes
      parsed documents and performs an action on them.  Normally, builders
      translate the documents to an output format, but it is also possible to
      use builders that e.g. check for broken links in the documentation, or
      build coverage information.

      See :doc:`/usage/builders/index` for an overview over Sphinx's built-in
      builders.

   configuration directory
      The directory containing :file:`conf.py`.  By default, this is the same as
      the :term:`source directory`, but can be set differently with the **-c**
      command-line option.
