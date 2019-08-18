import sphinx


def get_ref_xref_data(domain, node, target):
    """
    Use Sphinx's internals to resolve the reference and returns this data.

    :returns: tuple (``docname``, ``labelid``, ``sectname``)
    """
    if sphinx.version_info < (2, 1):
        # Borrowed from https://github.com/sphinx-doc/sphinx/blob/6ef08a42df4534dbb2664d49dc10a16f6df2acb2/sphinx/domains/std.py#L702-L711
        if node['refexplicit']:
            # reference to anonymous label; the reference uses
            # the supplied link caption
            docname, labelid = domain.data['anonlabels'].get(target, ('', ''))
            sectname = node.astext()
        else:
            # reference to named label; the final node will
            # contain the section name after the label
            docname, labelid, sectname = domain.data['labels'].get(target, ('', '', ''))
    else:
        # Borrowed from https://github.com/sphinx-doc/sphinx/blob/47cd262b3e50ed650a82f272ba128a1f872cda4d/sphinx/domains/std.py#L681-L689
        if node['refexplicit']:
            # reference to anonymous label; the reference uses
            # the supplied link caption
            docname, labelid = domain.anonlabels.get(target, ('', ''))
            sectname = node.astext()
        else:
            # reference to named label; the final node will
            # contain the section name after the label
            docname, labelid, sectname = domain.labels.get(target, ('', '', ''))
    return docname, labelid, sectname
