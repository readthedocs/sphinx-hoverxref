Changelog
=========

This page shows all the changes done on each version.


Version 0.8b1
-------------

* Move from TravisCI to CircleCI
* Use Read the Docs' Embed APIv3
* Stop adding ``data-`` attributes to HTML nodes
* Do not require ``hoverxref_project`` and ``hoverxref_version`` defined anymore
* Simplify code by removing ``HoverXRefHTMLTranslatorMixin`` override required and utils functions to get xref data
* Add new config ``hoverxref_sphinx_version`` used to send to Embed APIv3
* Update all Python requirements
* Remove via Javascript the ``title=`` property on Intersphinx references
* Support for ``glossary``/``term`` added
* Support for ``sphinxcontrib-bibtex`` added
* Improve documentation to show examples of documentation not hosted on Read the Docs
* Use regular expressions on tests to allow partial matching when required