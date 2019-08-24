from sphinx.domains.python import PythonDomain
from sphinx.domains.std import StandardDomain
from sphinx.util import logging
from .utils import get_ref_xref_data, get_ref_obj_data

logger = logging.getLogger(__name__)


class HoverXRefBaseDomain:

    def _is_hoverxref_configured(self, env):
        project = env.config.hoverxref_project
        version = env.config.hoverxref_version
        return project and version

    def _inject_hoverxref_data(self, env, refnode, docname, labelid):
        refnode.replace_attr('classes', ['hoverxref'])

        project = env.config.hoverxref_project
        version = env.config.hoverxref_version
        refnode._hoverxref = {
            'data-project': project,
            'data-version': version,
            'data-doc': docname,
            'data-section': labelid,
        }


class HoverXRefPythonDomain(HoverXRefBaseDomain, PythonDomain):

    def resolve_xref(self, env, fromdocname, builder, type, target, node, contnode):
        refnode = super().resolve_xref(env, fromdocname, builder, type, target, node, contnode)
        if refnode is None:
            return

        modname = node.get('py:module')
        clsname = node.get('py:class')
        searchmode = node.hasattr('refspecific') and 1 or 0
        matches = self.find_obj(env, modname, clsname, target,
                                type, searchmode)
        name, obj = matches[0]

        if self._is_hoverxref_configured(env):
            docname, labelid = obj[0], name
            self._inject_hoverxref_data(env, refnode, docname, labelid)
            logger.info(
                ':ref: _hoverxref injected: fromdocname=%s %s',
                fromdocname,
                refnode._hoverxref,
            )
        return refnode


class HoverXRefStandardDomain(HoverXRefBaseDomain, StandardDomain):
    """
    Override ``StandardDomain`` to save the values after the xref resolution.

    ``:ref:`` are treating as a different node in Sphinx
    (``sphinx.addnodes.pending_xref``). These nodes are translated to regular
    ``docsutils.nodes.reference`` for this domain class.

    Before loosing the data used to resolve the reference, our customized domain
    saves it inside the node itself to be used later by the ``HTMLTranslator``.
    """

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        if typ == 'hoverxref':
            resolver = self._resolve_ref_xref
            return resolver(env, fromdocname, builder, typ, target, node, contnode)

        return super().resolve_xref(env, fromdocname, builder, typ, target, node, contnode)

    # NOTE: We could override more ``_resolve_xref`` method apply hover in more places
    def _resolve_ref_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        refnode = super()._resolve_ref_xref(env, fromdocname, builder, typ, target, node, contnode)
        if refnode is None:
            return

        if not self._is_hoverxref_configured(env) and typ == 'hoverxref':
            # Using ``:hoverxref:`` role without having hoverxref configured
            # properly. Log a warning.
            logger.warning('hoverxref role is not fully configured.')

        if self._is_hoverxref_configured(env) and (env.config.hoverxref_auto_ref or typ == 'hoverxref'):
            docname, labelid, _ = get_ref_xref_data(self, node, target)
            self._inject_hoverxref_data(env, refnode, docname, labelid)
            logger.info(
                ':ref: _hoverxref injected: fromdocname=%s %s',
                fromdocname,
                refnode._hoverxref,
            )
        return refnode

    def _resolve_obj_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        refnode = super()._resolve_obj_xref(env, fromdocname, builder, typ, target, node, contnode)
        if refnode is None:
            return

        if typ in env.config.hoverxref_roles:
            docname, labelid = get_ref_obj_data(self, node, typ, target)
            if self._is_hoverxref_configured(env):
                self._inject_hoverxref_data(env, refnode, docname, labelid)
                logger.info(
                    ':%s: _hoverxref injected: fromdocname=%s %s',
                    typ,
                    fromdocname,
                    refnode._hoverxref,
                )
        return refnode
