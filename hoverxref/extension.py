import os
from sphinx.writers.html import HTMLTranslator
from sphinx.domains.std import StandardDomain


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
        refnode._hoverxref = {
            'data-project': project,
            'data-version': version,
            'data-doc': node.get('refdoc'),
            'data-section': node.get('reftarget'),
        }

        return refnode


class HoverXRefHTMLTranslator(HTMLTranslator):

    def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
        if tagname == 'a' and hasattr(node, '_hoverxref'):
            attributes.update(node._hoverxref)

        return super().starttag(node, tagname, suffix, empty, **attributes)


def setup(app):
    # Hovercard extension

    # ``override`` was introduced in 1.8
    app.require_sphinx('1.8')

    default_project = os.environ.get('READTHEDOCS_PROJECT')
    default_version = os.environ.get('READTHEDOCS_VERSION')
    app.add_config_value('hoverxref_project', default_project, 'html')
    app.add_config_value('hoverxref_version', default_version, 'html')

    app.set_translator('html', HoverXRefHTMLTranslator, override=True)
    app.add_domain(HoverXRefStandardDomain, override=True)

    app.add_js_file('js/tooltipster.bundle.min.js')
    app.add_js_file('js/main.js')
    app.add_css_file('css/tooltipster.bundle.min.css')
    app.add_css_file('css/tooltipster-sideTip-shadow.min.css')

    static_path = os.path.join(os.path.dirname(__file__), '_static')
    app.config.html_static_path.append(static_path)
