Usage
=====

This extension defines a custom role called ``:hoverxref:``.
When this role is used, it will show a tooltip [#]_ when the ``hover`` mouse event is triggered,
and will embed the content of the document/section the link is pointing to, into the tooltip's content.

``:hoverxref:`` role uses Sphinx's internals reference resolution to find out where the link points to.
So, the way of referencing the section works in the same way as the ``:ref:`` standard role.
See Sphinx's :rst:role:`ref` for more information.

Simplest usage example,

.. code-block:: rst

   This will :hoverxref:`show a tooltip <hoverxref:hoverxref>` in the linked words to ``hoverxref``.

will render to this:

This will :hoverxref:`show a tooltip <hoverxref:hoverxref>` in the linked words to ``hoverxref``.


Tooltip on intersphinx content
------------------------------

Sphinx comes with a nice built-in extension called :doc:`sphinx.ext.intersphinx <sphinx:usage/extensions/intersphinx>`
that allows you to generate links to specific objects in other project's documentation pages.

You can combine this extension with ``sphinx-hoverxref`` to show tooltips over these links to other projects.
For example, this documentation itself configures intersphinx with Read the Docs documentation and allow us
to do the following:

.. code-block:: rst

   Show a tooltip for :doc:`Read the Docs automation rules <readthedocs:automation-rules>`.

That will render to:

Show a tooltip for :doc:`Read the Docs automation rules <readthedocs:automation-rules>`.

.. note::

   Keep in mind that the linked project should be hosted at Read the Docs or,
   be one of the allowed external projects:
   currently CPython, SymPy, NumPy are supported.


Example with projects not hosted on Read the Docs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Show a tooltip for CPython documentation: :py:mod:`webbrowser <webbrowser>`.
* Show a tooltip for SymPy documentation: :py:class:`sympy.functions.combinatorial.numbers.tribonacci <sympy.functions.combinatorial.numbers.tribonacci>`.
* Show a tooltip for NumPy documentation: :py:class:`numpy.single <numpy.single>`.


Tooltip on custom object
------------------------

Sphinx has the ability to define custom objects (via :py:meth:`Sphinx.add_object_type <sphinx.application.Sphinx.add_object_type>`).
``hoverxref`` can also show a tooltip on these objects if desired.
You need to tell ``hoverxref`` which are the roles where the tooltip has to appear on.
To do this, use :confval:`hoverxref_roles <hoverxref_roles>` config.

Example
~~~~~~~

This documentation defines the ``confval`` role.
The role is used to define all the configurations of the extension.
These configurations are added to the Sphinx index and we can easily refer to them and show a tooltip.
This is reStructuredText code to do this:

.. code-block:: rst

   Show a tooltip to :confval:`hoverxref_auto_ref <hoverxref_auto_ref>` configuration.

the previous code will render to:

Show a tooltip to :confval:`hoverxref_auto_ref <hoverxref_auto_ref>` configuration.


Tooltip on all :ref: roles
--------------------------

If you want to show a tooltip in all the appearances of the ``:ref:`` role,
you have to set the configuration ``hoverxref_auto_ref = True`` in your ``conf.py`` file.

After setting that config, using ``:ref:`` will just render the tooltip:

.. code-block:: rst

   Show a tooltip to :ref:`usage:Tooltip on all :ref: roles` section on this page.

that reStructuredText code will render to:

Show a tooltip to :ref:`usage:Tooltip on all :ref: roles` page.

Tooltip on Sphinx Domains
-------------------------

You can decide whether use ``hoverxref`` on a particular Sphinx Domain as well.
An example using Python Domain would be like:

.. code-block:: rst

   :py:class:`hoverxref.domains.HoverXRefStandardDomainMixin`

That will render to:

:py:class:`hoverxref.domains.HoverXRefStandardDomainMixin`


To enable ``hoverxref`` on a domain, you need to use the config :confval:`hoverxref_domains`
indicating which are the domains you desire.


Tooltip on glossary terms
-------------------------

You can add tooltips to glossary terms:

.. code-block:: rst

   See the :term:`sphinx:environment` definition in the glossary.

That will render to:

See the :term:`sphinx:environment` definition in the glossary.

To enable ``hoverxref`` on glossary terms, you need to add ``'term'`` to :confval:`hoverxref_roles`.


Tooltip on sphinxcontrib-bibtex cites
-------------------------------------

If you want to show a tooltip on `sphinxcontrib-bibtex <https://sphinxcontrib-bibtex.readthedocs.io/en/latest/>`_ cites,
you just need to enable it in :confval:`hoverxref_domains` by adding ``'cite'`` to that list.
Example:

.. code-block:: rst

   See :cite:t:`1987:nelson` for an introduction to non-standard analysis.
   Non-standard analysis is fun :cite:p:`1987:nelson`.

See :cite:t:`1987:nelson` for an introduction to non-standard analysis.
Non-standard analysis is fun :cite:p:`1987:nelson`.

.. note::

   Note that tooltips on sphinxcontrib-bibtex are supported on ``Sphinx>=2.1`` only.

.. bibliography::


Tooltip with content that needs extra rendering steps
-----------------------------------------------------

Since ``hoverxref`` supports including arbitrary HTML,
you may find that it could be possible that there are some content that it's not well rendered inside the tooltip.
If this is the case, it may be because there are some extra actions that needs to be done after the content is injected in the tooltip.

These actions are usually calling a Javascript function.
``hoverxref`` is prepared to support this type of content and currently supports rendering
`sphinx-tabs`_ and mathjax_.

.. warning::

   Note that Sphinx>=3.5 adds `a feature to only include JS/CSS in pages where they are used`_ instead of in all the pages.
   This `may affect the rendering of tooltips`_ that includes content requiring extra rendering steps.
   **Make sure you are using Sphinx <=3.4.x or >=4.1.x** if you require rendering this type of content in your tooltips.

   .. _a feature to only include JS/CSS in pages where they are used: https://github.com/sphinx-doc/sphinx/pull/8631
   .. _may affect the rendering of tooltips: https://github.com/sphinx-doc/sphinx/issues/9115


Tooltip with ``sphinx-tabs``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To render a tooltip with a ``sphinx-tabs`` content you need to enable :confval:`hoverxref_sphinxtabs`.

.. code-block:: rst

   Show a :ref:`tooltip with Sphinx Tabs <installation:Installation>` on its content.

Show a :ref:`tooltip with Sphinx Tabs <installation:Installation>` on its content.


Tooltip with ``mathjax``
~~~~~~~~~~~~~~~~~~~~~~~~

To render a tooltip where its contents has a ``mathjax`` you need to enable :confval:`hoverxref_mathjax`.

.. code-block:: rst

   Show a :hoverxref:`tooltip with Mathjax <mathjax:Mathjax>` formulas.

Show a :hoverxref:`tooltip with Mathjax <mathjax:Mathjax>` formulas.


.. _sphinx-tabs: https://github.com/djungelorm/sphinx-tabs
.. _mathjax: http://www.sphinx-doc.org/es/master/usage/extensions/math.html#module-sphinx.ext.mathjax

.. [#] we use tooltips as a generic word, but we refer to both, tooltips and modal dialogues
