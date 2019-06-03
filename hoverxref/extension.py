import os
from sphinx.domains.std import StandardDomain
from sphinx.util.fileutil import copy_asset
from sphinx.writers.html import HTMLTranslator

ASSETS_FILES = [
    'js/tooltipster.bundle.min.js',
    'js/hoverxref.js_t',
    'css/tooltipster.bundle.min.css',
    'css/tooltipster-sideTip-shadow.min.css',
]


class HoverXRefStandardDomain(StandardDomain):

    # NOTE: We could override more ``_resolve_xref`` method apply hover in more places
    def _resolve_ref_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        refnode = super()._resolve_ref_xref(env, fromdocname, builder, typ, target, node, contnode)
        if refnode is None:
            return

        project = env.config.hoverxref_project
        version = env.config.hoverxref_version

        if not project or not version:
            return refnode

        refnode.replace_attr('classes', ['hoverxref'])

        # TODO: consider other cases of ``:ref:`` usage
        reftarget = doc = section = node.get('reftarget')
        if ':' in reftarget:
            doc, section = reftarget.split(':', 1)

        refnode._hoverxref = {
            'data-project': project,
            'data-version': version,
            'data-doc': doc,
            'data-section': section,
        }

        return refnode


class HoverXRefHTMLTranslator(HTMLTranslator):

    def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
        if tagname == 'a' and hasattr(node, '_hoverxref'):
            attributes.update(node._hoverxref)

        return super().starttag(node, tagname, suffix, empty, **attributes)


def copy_asset_files(app, exception):
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


def setup(app):
    # Hovercard extension

    # ``override`` was introduced in 1.8
    app.require_sphinx('1.8')

    default_project = os.environ.get('READTHEDOCS_PROJECT')
    default_version = os.environ.get('READTHEDOCS_VERSION')
    app.add_config_value('hoverxref_project', default_project, 'html')
    app.add_config_value('hoverxref_version', default_version, 'html')

    app.add_config_value('hoverxref_tooltip_theme', 'tooltipster-shadow', 'env')
    app.add_config_value('hoverxref_tooltip_interactive', True, 'env')
    app.add_config_value('hoverxref_tooltip_maxwidth', 450, 'env')
    app.add_config_value('hoverxref_tooltip_animation', 'fade', 'env')
    app.add_config_value('hoverxref_tooltip_animation_duration', 0, 'env')
    app.add_config_value('hoverxref_tooltip_content', 'Loading...', 'env')

    app.set_translator('html', HoverXRefHTMLTranslator, override=True)
    app.add_domain(HoverXRefStandardDomain, override=True)

    app.connect('build-finished', copy_asset_files)

    for f in ASSETS_FILES:
        if f.endswith('.js') or f.endswith('.js_t'):
            app.add_js_file(f.replace('.js_t', '.js'))
        if f.endswith('.css'):
            app.add_css_file(f)
