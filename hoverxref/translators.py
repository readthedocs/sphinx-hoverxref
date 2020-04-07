from sphinx.util import logging

logger = logging.getLogger(__name__)


class HoverXRefHTMLTranslatorMixin:

    """
    Mixin ``HTMLTranslator`` to render extra data saved in reference nodes.

    It adds all the values saved under ``_hoverxref`` as attributes of the HTML
    reference tag.
    """

    def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
        if tagname == 'a' and hasattr(node, '_hoverxref'):
            attributes.update(node._hoverxref)
            logger.info('_hoverxref attributes: %s', attributes)

        return super().starttag(node, tagname, suffix, empty, **attributes)
