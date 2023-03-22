Changelog
=========

This page shows all the changes done on each version.

Version 1.3.0
-------------

* Handle explicit intersphinx inventory names in all domains --not just ``std`` (https://github.com/readthedocs/sphinx-hoverxref/pull/236)

Version 1.2.0
-------------

* New config ``hoverxref_tooltip_lazy`` to improve large page experience (https://github.com/readthedocs/sphinx-hoverxref/pull/227/)

Version 1.1.3
-------------

* Ignore ``pending_xref`` (missing references) that don't have domains (https://github.com/readthedocs/sphinx-hoverxref/pull/210)

Version 1.1.2
-------------

* Prefix all the CSS classes with ``hxr-`` to avoid collisions with other frameworks

Version 1.1.1
-------------

* Fix an issue with intersphinx and domains when the ``reftype`` was unknown

Version 1.1.0
-------------

* Improve intersphinx robustness
* Update all dependencies for building documentation
* Packaging: use bumpver and flit to build/publish
* Improve documentation installing instructions
* Setup pip-tools together with dependabot to handle dependencies updates
* Remove tests for Python 3.6 and Python 3.7 and add newer Sphinx versions (4.4, 4.5 and 5.0)

Version 1.0.1
-------------

*  Ajax header: send the header on each call instead with .ajaxSetup (https://github.com/readthedocs/sphinx-hoverxref/pull/167)
*  Tests: solve problem with RTD documentation's title (https://github.com/readthedocs/sphinx-hoverxref/pull/168)

Version 1.0.0
-------------

* Official release

Version 0.9b1
-------------

* Send ``X-HoverXRef-Version`` HTTP header when hitting the API


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
