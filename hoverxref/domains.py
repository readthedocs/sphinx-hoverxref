from sphinx.util import logging
from .utils import get_ref_xref_data, get_ref_obj_data, get_ref_numref_data

logger = logging.getLogger(__name__)


class HoverXRefBaseDomain:

    hoverxref_types = (
        'hoverxref',
        'hoverxreftooltip',
        'hoverxrefmodal',
    )

    def _inject_hoverxref_data(self, env, refnode, typ, docname, docpath, labelid):
        classes = ['hoverxref']
        type_class = None
        if typ == 'hoverxreftooltip':
            type_class = 'tooltip'
            classes.append(type_class)
        elif typ == 'hoverxrefmodal':
            type_class = 'modal'
            classes.append(type_class)
        if not type_class:
            type_class = env.config.hoverxref_role_types.get(typ)
            if not type_class:
                default = env.config.hoverxref_default_type
                type_class = default
                logger.info(
                    'Using default style (%s) for unknown typ (%s). '
                    'Define it in hoverxref_role_types.',
                    default,
                    typ,
                )
            classes.append(type_class)

        refnode.replace_attr('classes', classes)

        project = env.config.hoverxref_project
        version = env.config.hoverxref_version
        refnode._hoverxref = {
            'data-project': project,
            'data-version': version,
            'data-doc': docname,
            'data-docpath': docpath,
            'data-section': labelid,
        }

    def _get_docpath(self, builder, docname):
        docpath = builder.get_outfilename(docname)
        docpath = docpath.replace(builder.outdir, '')
        return docpath

    def _is_ignored_ref(self, env, target):
        # HACK: skip all references if the builder is non-html. We shouldn't
        # have overridden the Domain in first instance at ``setup_domains``
        # function, but at that time ``app.builder`` is not yet initialized. If
        # we suscribe ourselves to ``builder-initied`` it's too late and our
        # override does not take effect. Other builders (e.g. LatexBuilder) may
        # fail with internal functions we use (e.g. builder.get_outfilename).
        # So, we are skipping it here :(
        if env.app.builder.format != 'html':
            return True

        if target in env.config.hoverxref_ignore_refs:
            logger.info(
                'Ignoring reference in hoverxref_ignore_refs. target=%s',
                target,
            )
            return True
        return False


class HoverXRefPythonDomainMixin(HoverXRefBaseDomain):

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        refnode = super().resolve_xref(env, fromdocname, builder, typ, target, node, contnode)
        if refnode is None:
            return refnode

        if any([
                not env.config.hoverxref_is_configured,
                self._is_ignored_ref(env, target),
        ]):
            return refnode

        modname = node.get('py:module')
        clsname = node.get('py:class')
        searchmode = node.hasattr('refspecific') and 1 or 0
        matches = self.find_obj(env, modname, clsname, target,
                                typ, searchmode)
        name, obj = matches[0]

        docname, labelid = obj[0], name
        docpath = self._get_docpath(builder, docname)
        self._inject_hoverxref_data(env, refnode, typ, docname, docpath, labelid)
        logger.debug(
            ':ref: _hoverxref injected: fromdocname=%s %s',
            fromdocname,
            refnode._hoverxref,
        )
        return refnode


class HoverXRefStandardDomainMixin(HoverXRefBaseDomain):
    """
    Mixin for ``StandardDomain`` to save the values after the xref resolution.

    ``:ref:`` are treating as a different node in Sphinx
    (``sphinx.addnodes.pending_xref``). These nodes are translated to regular
    ``docsutils.nodes.reference`` for this domain class.

    Before loosing the data used to resolve the reference, our customized domain
    saves it inside the node itself to be used later by the ``HTMLTranslator``.
    """

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        if typ in self.hoverxref_types:
            resolver = self._resolve_ref_xref
            return resolver(env, fromdocname, builder, typ, target, node, contnode)

        return super().resolve_xref(env, fromdocname, builder, typ, target, node, contnode)

    # NOTE: We could override more ``_resolve_xref`` method apply hover in more places
    def _resolve_ref_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        refnode = super()._resolve_ref_xref(env, fromdocname, builder, typ, target, node, contnode)
        if refnode is None:
            return refnode

        if any([
                not env.config.hoverxref_is_configured,
                self._is_ignored_ref(env, target),
                not (env.config.hoverxref_auto_ref or typ in self.hoverxref_types)
        ]):
            return refnode


        docname, labelid, _ = get_ref_xref_data(self, node, target)
        docpath = self._get_docpath(builder, docname)
        self._inject_hoverxref_data(env, refnode, typ, docname, docpath, labelid)
        logger.debug(
            ':ref: _hoverxref injected: fromdocname=%s %s',
            fromdocname,
            refnode._hoverxref,
        )
        return refnode

    def _resolve_obj_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        refnode = super()._resolve_obj_xref(env, fromdocname, builder, typ, target, node, contnode)
        if refnode is None:
            return refnode

        if any([
                not env.config.hoverxref_is_configured,
                self._is_ignored_ref(env, target),
                typ not in env.config.hoverxref_roles,
        ]):
            return refnode

        docname, labelid = get_ref_obj_data(self, node, typ, target)
        docpath = self._get_docpath(builder, docname)
        self._inject_hoverxref_data(env, refnode, typ, docname, docpath, labelid)
        logger.debug(
            ':%s: _hoverxref injected: fromdocname=%s %s',
            typ,
            fromdocname,
            refnode._hoverxref,
        )
        return refnode

    # TODO: combine this method with ``_resolve_obj_xref``
    def _resolve_numref_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        refnode = super()._resolve_numref_xref(env, fromdocname, builder, typ, target, node, contnode)
        if refnode is None:
            return refnode

        if any([
                not env.config.hoverxref_is_configured,
                self._is_ignored_ref(env, target),
                typ not in env.config.hoverxref_roles,
        ]):
            return refnode

        docname, labelid = get_ref_numref_data(self, node, typ, target)
        docpath = self._get_docpath(builder, docname)
        self._inject_hoverxref_data(env, refnode, typ, docname, docpath, labelid)
        logger.debug(
            ':%s: _hoverxref injected: fromdocname=%s %s',
            typ,
            fromdocname,
            refnode._hoverxref,
        )
        return refnode
