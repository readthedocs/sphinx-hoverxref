Configuration
=============

The default settings should be enough for most of the cases.
For more specific use cases, you can customize these configuration options in your ``conf.py`` file:

.. confval:: hoverxref_project

   Description: Read the Docs project slug

   Default: It defaults to ``READTHEDOCS_PROJECT`` environment variable

   Type: string

.. confval:: hoverxref_version

   Description: Read the Docs version slug

   Default: It defaults to ``READTHEDOCS_VERSION`` environment variable

   Type: string

.. confval:: hoverxref_tooltip_api_host

   Description: Host URL for the API to retrieve the tooltip content

   Default: ``https://readthedocs.org``

   Type: string

.. confval:: hoverxref_auto_ref

   Description: Make all ``:ref:`` role to show a tooltip

   Default: ``False``

   Type: bool

.. warning::

   The following settings are passed directly to Tooltipster_. See https://iamceege.github.io/tooltipster/#options for more information about their descriptions.

.. confval:: hoverxref_tooltip_theme

   Default: ``['tooltipster-shadow', 'tooltipster-shadow-custom']``

   Type: list of strings

.. confval:: hoverxref_tooltip_interactive

   Default: ``True``

   Type: bool

.. confval:: hoverxref_tooltip_maxwith

   Default: ``450``

   Type: int

.. confval:: hoverxref_tooltip_animation

   Default: ``fade``

   Type: string

.. confval:: hoverxref_tooltip_animation_duration

   Default: ``0``

   Type: int

.. confval:: hoverxref_tooltip_content

   Default: ``Loading...``

   Type: string

.. _Tooltipster: https://iamceege.github.io/tooltipster/
