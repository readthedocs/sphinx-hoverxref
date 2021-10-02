Configuration
=============

The default settings should be enough for most of the cases.
For more specific use cases, you can customize these configuration options in your ``conf.py`` file.

.. contents:: Table of contents
   :local:
   :backlinks: none
   :depth: 1

General settings
----------------

These settings are global and have effect on both, tooltips and modal dialogues.

.. confval:: hoverxref_role_types

   Description: Style to use by default when hover each type of reference (role).

   Default: ``{}``

   Type: dictionary

   Example:

   .. code-block:: python

      {
          'hoverxref': 'modal',
          'ref': 'modal',  # for hoverxref_auto_ref config
          'confval': 'tooltip',  # for custom object
          'mod': 'tooltip',  # for Python Sphinx Domain
          'class': 'tooltip',  # for Python Sphinx Domain
      }


.. confval:: hoverxref_default_type

   Description: Default style when the specific one was not found in :confval:`hoverxref_role_types`.

   Default: ``tooltip``

   Options: ``tooltip`` or ``modal``

   Type: string

.. confval:: hoverxref_auto_ref

   Description: Make all ``:ref:`` role to show a tooltip.

   Default: ``False``

   Type: bool

.. confval:: hoverxref_ignore_refs

   Description: Ignore to add tooltip on specific references. Useful when using :confval:`hoverxref_auto_ref`

   Default: ``['genindex', 'modindex', 'search']``

   Type: list

.. confval:: hoverxref_domains

   Description: List containing the Sphinx Domain's names where ``hoverxref`` has to be applied.

   Default: ``[]``

   Type: list

.. confval:: hoverxref_roles

   Description: List containing roles where ``hoverxref`` has to be applied.

   Default: ``[]``

   Type: list

   Example:

   .. code-block:: python

      hoverxref_roles = [
          'numref',
          'confval',
          'setting',
      ]

.. confval:: hoverxref_intersphinx

   Description: Enable Sphinx's hoverxref extension on intersphinx targets from ``intersphinx_mapping``.

   Default: ``[]``

   Type: list

   .. warning::

      The Sphinx's target project **must be hosted on Read the Docs** to work or,
      be one of the allowed external projects:
      currently CPython, SymPy, NumPy are supported.

.. confval:: hoverxref_intersphinx_types

   Description: Style used for intersphinx links.

   Default: ``{}``. It uses :confval:`hoverxref_default_type` if the intersphinx target is not defined in this config.

   Type: dict

   Example:

   .. code-block:: python

      {
          # make specific links to use a particular tooltip type
          'readthdocs': {
              'doc': 'modal',
              'ref': 'tooltip',
          },
          'python': {
              'class': 'modal',
              'ref':, 'tooltip',
          },

          # make all links for Sphinx to be ``tooltip``
          'sphinx': 'tooltip',
      }

.. confval:: hoverxref_sphinxtabs

   Description: Trigger an extra step to render tooltips where its content has a `Sphinx Tabs`_

   Default: ``False``

   Type: bool

.. _Sphinx Tabs: https://github.com/djungelorm/sphinx-tabs

.. confval:: hoverxref_mathjax

   Description: Trigger an extra step to render tooltips where its content has a `Mathjax`_

   Default: ``False``

   Type: bool

.. _Mathjax: http://www.sphinx-doc.org/es/master/usage/extensions/math.html#module-sphinx.ext.mathjax


.. confval:: hoverxref_api_host

   Description: Host URL for the API to retrieve the content of the floating window

   .. warning::

     You shouldn't modify this setting unless you know what you are doing.
     Its default should be fine to build the documentation and make it work in Read the Docs.

   Default: ``https://readthedocs.org``

   Type: string


Tooltipster
-----------

These settings have effect only in tooltips.

.. confval:: hoverxref_tooltip_class

   Description: CSS class to add to ``div`` created for the tooltip

   Default: ``rst-content``

   Type: string


.. warning::

   The following settings are passed directly to Tooltipster_.
   See `its options <https://www.heteroclito.fr/modules/tooltipster/#options>`_ for more information about their descriptions.

.. confval:: hoverxref_tooltip_theme

   Default: ``['tooltipster-shadow', 'tooltipster-shadow-custom']``

   Type: list of strings

.. confval:: hoverxref_tooltip_interactive

   Default: ``True``

   Type: bool

.. confval:: hoverxref_tooltip_maxwith

   Default: ``450``

   Type: int

.. confval:: hoverxref_tooltip_side

   Default: ``right``

   Type: string

.. confval:: hoverxref_tooltip_animation

   Default: ``fade``

   Type: string

.. confval:: hoverxref_tooltip_animation_duration

   Default: ``0``

   Type: int

.. confval:: hoverxref_tooltip_content

   Default: ``Loading...``

   Type: string

.. _Tooltipster: https://www.heteroclito.fr/modules/tooltipster/


MicroModal.js
-------------

These settings have effect only in modal dialogues.

.. confval:: hoverxref_modal_hover_delay

   Description: Delay time (in milliseconds) before showing the modal when hover over a ref

   Default: ``350``

   Type: int

.. confval:: hoverxref_modal_default_title

   Description: Title shown when the content does not have one

   Default: ``Note``

   Type: string

.. confval:: hoverxref_modal_prefix_title

   Description: Prefix included in the title of the modal

   Default: 📝 (ends with a trailing space)

   Type: string

.. confval:: hoverxref_modal_class

   Description:

   Default: ``rst-content``

   Type: string


.. warning::

   The following settings are passed directly to `MicroModal.js`_.
   See https://micromodal.now.sh/#configuration for more information about their descriptions.

.. confval:: hoverxref_modal_onshow_function

   Default: ``None``

   Type: string

.. confval:: hoverxref_modal_openclass

   Default: ``is-open``

   Type: string

.. confval:: hoverxref_modal_disable_focus

   Default: ``True``

   Type: bool

.. confval:: hoverxref_modal_disable_scroll

   Default: ``False``

   Type: bool

.. confval:: hoverxref_modal_awaitopenanimation

   Default: ``False``

   Type: bool

.. confval:: hoverxref_modal_awaitcloseanimation

   Default: ``False``

   Type: bool

.. confval:: hoverxref_modal_debugmode

   Default: ``False``

   Type: bool
