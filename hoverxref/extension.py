import os
import inspect
import types
from docutils import nodes
import sphinx
from sphinx.roles import XRefRole
from sphinx.util.fileutil import copy_asset
from sphinx.util import logging

from . import version
from .domains import (
    HoverXRefBaseDomain,
    HoverXRefPythonDomainMixin,
    HoverXRefStandardDomainMixin,
)
from .translators import HoverXRefHTMLTranslatorMixin

logger = logging.getLogger(__name__)


HOVERXREF_ASSETS_FILES = [
    'js/hoverxref.js_t',  # ``_t`` tells Sphinx this is a template
]

TOOLTIP_ASSETS_FILES = [
    # Tooltipster's Styles
    'js/tooltipster.bundle.min.js',
    'css/tooltipster.custom.css',
    'css/tooltipster.bundle.min.css',

    # Tooltipster's Themes
    'css/tooltipster-sideTip-shadow.min.css',
    'css/tooltipster-sideTip-punk.min.css',
    'css/tooltipster-sideTip-noir.min.css',
    'css/tooltipster-sideTip-light.min.css',
    'css/tooltipster-sideTip-borderless.min.css',
]

MODAL_ASSETS_FILES = [
    'js/micromodal.min.js',
    'css/micromodal.css',
]

ASSETS_FILES = HOVERXREF_ASSETS_FILES + TOOLTIP_ASSETS_FILES + MODAL_ASSETS_FILES

def copy_asset_files(app, exception):
    """
    Copy all assets after build finished successfully.

    Assets that are templates (ends with ``_t``) are previously rendered using
    using all the configs starting with ``hoverxref_`` as a context.
    """
    if exception is None:  # build succeeded

        context = {}
        for attr in app.config.values:
            if attr.startswith('hoverxref_'):
                # First, add the default values to the context
                context[attr] = app.config.values[attr][0]

        for attr in dir(app.config):
            if attr.startswith('hoverxref_'):
                # Then, add the values that the user overrides
                context[attr] = getattr(app.config, attr)

        # Finally, add some non-hoverxref extra configs
        configs = ['html_theme']
        for attr in configs:
            context[attr] = getattr(app.config, attr)

        for f in ASSETS_FILES:
            path = os.path.join(os.path.dirname(__file__), '_static', f)
            copy_asset(
                path,
                os.path.join(app.outdir, '_static', f.split('.')[-1].replace('js_t', 'js')),
                context=context,
            )


def setup_domains(app, config):
    """
    Override domains respecting the one defined (if any).

    We create a new class by inheriting the Sphinx Domain already defined
    and our own ``HoverXRef...DomainMixin`` that includes the logic for
    ``_hoverxref`` attributes.
    """
    # Add ``hoverxref`` role replicating the behavior of ``ref``
    for role in HoverXRefBaseDomain.hoverxref_types:
        app.add_role_to_domain(
            'std',
            role,
            XRefRole(
                lowercase=True,
                innernodeclass=nodes.inline,
                warn_dangling=True,
            ),
        )

    domain = types.new_class(
        'HoverXRefStandardDomain',
        (
            HoverXRefStandardDomainMixin,
            app.registry.domains.get('std'),
        ),
        {}
    )
    app.add_domain(domain, override=True)

    if 'py' in app.config.hoverxref_domains:
        domain = types.new_class(
            'HoverXRefPythonDomain',
            (
                HoverXRefPythonDomainMixin,
                app.registry.domains.get('py'),
            ),
            {}
        )
        app.add_domain(domain, override=True)


def setup_sphinx_tabs(app, config):
    """
    Disconnect ``update_context`` function from ``sphinx-tabs``.

    Sphinx Tabs removes the CSS/JS from pages that does not use the directive.
    Although, we need them to use inside the tooltip.
    """
    if sphinx.version_info < (3, 0, 0):
        listeners = list(app.events.listeners.get('html-page-context').items())
    else:
        listeners = [
            (listener.id, listener.handler)
            for listener in app.events.listeners.get('html-page-context')
        ]
    for listener_id, function in listeners:
        module_name = inspect.getmodule(function).__name__
        if module_name == 'sphinx_tabs.tabs':
            app.disconnect(listener_id)


def setup_translators(app):
    """
    Override translators respecting the one defined (if any).

    We create a new class by inheriting the Sphinx Translator already defined
    and our own ``HoverXRefHTMLTranslatorMixin`` that includes the logic to
    ``_hoverxref`` attributes.
    """

    if app.builder.format != 'html':
        # do not modify non-html builders
        return

    for name, klass in app.registry.translators.items():
        translator = types.new_class(
            'HoverXRefHTMLTranslator',
            (
                HoverXRefHTMLTranslatorMixin,
                klass,
            ),
            {},
        )
        app.set_translator(name, translator, override=True)

    translator = types.new_class(
        'HoverXRefHTMLTranslator',
        (
            HoverXRefHTMLTranslatorMixin,
            app.builder.default_translator_class,
        ),
        {},
    )
    app.set_translator(app.builder.name, translator, override=True)



def is_hoverxref_configured(app, config):
    """
    Save a config if hoverxref is properly configured.

    It checks for ``hoverxref_project`` and ``hoverxref_version`` being defined
    and set ``hoverxref_is_configured=True`` if configured.
    """
    config.hoverxref_is_configured = True

    project = config.hoverxref_project
    version = config.hoverxref_version
    if not project or not version:
        config.hoverxref_is_configured = False
        # ``hoverxref`` extension is not fully configured
        logger.info(
            'hoverxref extension is not fully configured. '
            'Tooltips may not work as expected. '
            'Check out the documentation for hoverxref_project and hoverxref_version configuration options.',
        )


def setup_theme(app, exception):
    """
    Auto-configure default settings for known themes.

    Add a small custom CSS file for a specific theme and set hoverxref configs
    (if not overwritten by the user) with better defaults for these themes.
    """
    css_file = None
    theme = app.config.html_theme
    default, rebuild, types = app.config.values.get('hoverxref_modal_class')
    if theme == 'sphinx_material':
        if app.config.hoverxref_modal_class == default:
            app.config.hoverxref_modal_class = 'md-typeset'
            css_file = 'css/sphinx_material.css'
    elif theme == 'alabaster':
        if app.config.hoverxref_modal_class == default:
            app.config.hoverxref_modal_class = 'body'
            css_file = 'css/alabaster.css'
    elif theme == 'sphinx_rtd_theme':
        if app.config.hoverxref_modal_class == default:
            css_file = 'css/sphinx_rtd_theme.css'

    if css_file:
        app.add_css_file(css_file)
        path = os.path.join(os.path.dirname(__file__), '_static', css_file)
        copy_asset(
            path,
            os.path.join(app.outdir, '_static', 'css'),
        )


def deprecated_configs_warning(app, exception):
    """Log warning message if old configs are used."""
    default, rebuild, types = app.config.values.get('hoverxref_tooltip_api_host')
    if app.config.hoverxref_tooltip_api_host != default:
        message = '"hoverxref_tooltip_api_host" is deprecated and replaced by "hoverxref_api_host".'
        logger.warning(message)
        app.config.hoverxref_api_host = app.config.hoverxref_tooltip_api_host



def setup(app):
    """Setup ``hoverxref`` Sphinx extension."""

    # ``override`` was introduced in 1.8
    app.require_sphinx('1.8')

    default_project = os.environ.get('READTHEDOCS_PROJECT')
    default_version = os.environ.get('READTHEDOCS_VERSION')
    app.add_config_value('hoverxref_project', default_project, 'html')
    app.add_config_value('hoverxref_version', default_version, 'html')
    app.add_config_value('hoverxref_auto_ref', False, 'env')
    app.add_config_value('hoverxref_mathjax', False, 'env')
    app.add_config_value('hoverxref_sphinxtabs', False, 'env')
    app.add_config_value('hoverxref_roles', [], 'env')
    app.add_config_value('hoverxref_domains', [], 'env')
    app.add_config_value('hoverxref_ignore_refs', ['genindex', 'modindex', 'search'], 'env')
    app.add_config_value('hoverxref_role_types', {}, 'env')
    app.add_config_value('hoverxref_default_type', 'tooltip', 'env')
    app.add_config_value('hoverxref_api_host', 'https://readthedocs.org', 'env')

    # Tooltipster settings
    # Deprecated in favor of ``hoverxref_api_host``
    app.add_config_value('hoverxref_tooltip_api_host', 'https://readthedocs.org', 'env')
    app.add_config_value('hoverxref_tooltip_theme', ['tooltipster-shadow', 'tooltipster-shadow-custom'], 'env')
    app.add_config_value('hoverxref_tooltip_interactive', True, 'env')
    app.add_config_value('hoverxref_tooltip_maxwidth', 450, 'env')
    app.add_config_value('hoverxref_tooltip_side', 'right', 'env')
    app.add_config_value('hoverxref_tooltip_animation', 'fade', 'env')
    app.add_config_value('hoverxref_tooltip_animation_duration', 0, 'env')
    app.add_config_value('hoverxref_tooltip_content', 'Loading...', 'env')
    app.add_config_value('hoverxref_tooltip_class', 'rst-content', 'env')

    # MicroModal settings
    app.add_config_value('hoverxref_modal_hover_delay', 350, 'env')
    app.add_config_value('hoverxref_modal_class', 'rst-content', 'env')
    app.add_config_value('hoverxref_modal_onshow_function', None, 'env')
    app.add_config_value('hoverxref_modal_openclass', 'is-open', 'env')
    app.add_config_value('hoverxref_modal_disable_focus', True, 'env')
    app.add_config_value('hoverxref_modal_disable_scroll', False, 'env')
    app.add_config_value('hoverxref_modal_awaitopenanimation', False, 'env')
    app.add_config_value('hoverxref_modal_awaitcloseanimation', False, 'env')
    app.add_config_value('hoverxref_modal_debugmode', False, 'env')
    app.add_config_value('hoverxref_modal_default_title', 'Note', 'env')
    app.add_config_value('hoverxref_modal_prefix_title', '📝 ', 'env')

    app.connect('builder-inited', setup_translators)

    app.connect('config-inited', deprecated_configs_warning)

    app.connect('config-inited', setup_domains)
    app.connect('config-inited', setup_sphinx_tabs)
    app.connect('config-inited', is_hoverxref_configured)
    app.connect('config-inited', setup_theme)
    app.connect('build-finished', copy_asset_files)

    for f in ASSETS_FILES:
        if f.endswith('.js') or f.endswith('.js_t'):
            app.add_js_file(f.replace('.js_t', '.js'))
        if f.endswith('.css'):
            app.add_css_file(f)

    return {
        'version': version,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
