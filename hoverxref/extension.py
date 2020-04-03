import os
import inspect
from docutils import nodes
from sphinx.roles import XRefRole
from sphinx.util.fileutil import copy_asset

from . import version
from .domains import HoverXRefPythonDomain, HoverXRefStandardDomain
from .translators import HoverXRefHTMLTranslator

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

        for f in ASSETS_FILES:
            path = os.path.join(os.path.dirname(__file__), '_static', f)
            copy_asset(
                path,
                os.path.join(app.outdir, '_static', f.split('.')[-1].replace('js_t', 'js')),
                context=context,
            )


def setup_domains(app, config):
    # Add ``hoverxref`` role replicating the behavior of ``ref``
    app.add_role_to_domain(
        'std',
        'hoverxref',
        XRefRole(
            lowercase=True,
            innernodeclass=nodes.inline,
            warn_dangling=True,
        ),
    )
    app.add_domain(HoverXRefStandardDomain, override=True)

    if 'py' in config.hoverxref_domains:
        app.add_domain(HoverXRefPythonDomain, override=True)


def setup_sphinx_tabs(app, config):
    """
    Disconnect ``update_context`` function from ``sphinx-tabs``.

    Sphinx Tabs removes the CSS/JS from pages that does not use the directive.
    Although, we need them to use inside the tooltip.
    """
    listeners = list(app.events.listeners.get('html-page-context').items())
    for listener_id, function in listeners:
        module_name = inspect.getmodule(function).__name__
        if module_name == 'sphinx_tabs.tabs':
            app.disconnect(listener_id)


def setup_theme(app, exception):
    """
    Auto-configure default settings for known themes.

    Add a small custom CSS file for a specific theme and set hoverxref configs
    (if not overwritten by the user) with better defaults for these themes.
    """
    if app.config.hoverxref_type != 'modal':
        return

    css_file = None
    theme = app.config.html_theme
    default, rebuild, types = app.config.values.get('hoverxref_modal_class')
    if theme == 'sphinx_material':
        if app.config.hoverxref_modal_class == default:
            app.config.hoverxref_modal_class = 'md-typeset'
            css_file = 'css/material.css'
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
    app.add_config_value('hoverxref_type', 'tooltip', 'env')

    # Tooltipster settings
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

    app.set_translator('html', HoverXRefHTMLTranslator, override=True)

    # Read the Docs use ``readthedocs`` as the name of the build, so we need to
    # replace this as well
    app.set_translator('readthedocs', HoverXRefHTMLTranslator, override=True)
    app.set_translator('readthedocsdirhtml', HoverXRefHTMLTranslator, override=True)

    app.connect('config-inited', setup_domains)
    app.connect('config-inited', setup_sphinx_tabs)
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
