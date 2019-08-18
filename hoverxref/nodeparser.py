from sphinx import addnodes
from hoverxref.registry import registry


def parse_node(name):
    """
    Function to use as ``parse_node`` argument for ``Sphinx.add_object_type``.

    When a new object is defined, using this helper function allows to add the
    HTML tag id into the ``dl`` instead of the ``dt`` and so the whole section
    is returned as content for the tooltip.
    """
    registry.add_object_type(name)

    def object_parse_node(env, string, node):
        node += addnodes.desc_name(string, string)

        # By default the structure that Sphinx creates put the ids in the inner
        # ``dt`` HTML tag. This makes the Read the Docs API to return just the title
        # of it instead the full content. Here, we put the ids in the outer ``dl``
        # HTML tag instead.
        node_id = '{name}-{string}'.format(name=name, string=string)
        node.parent['ids'].append(node_id)
        return string

    return object_parse_node
