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


def get_ref_obj_data(domain, node, typ, target):
    """
    Use Sphinx's internals to resolve an object reference and returns this data.

    :returns: tuple (``docname``, ``labelid``)
    """
    objtypes = domain.objtypes_for_role(typ) or []
    if sphinx.version_info < (2, 1):
        # Borrowed from https://github.com/sphinx-doc/sphinx/blob/6ef08a42df4534dbb2664d49dc10a16f6df2acb2/sphinx/domains/std.py#L851-L855
        for objtype in objtypes:
            if (objtype, target) in domain.data['objects']:
                docname, labelid = domain.data['objects'][objtype, target]
                break
    else:
        # Borrowed from https://github.com/sphinx-doc/sphinx/blob/47cd262b3e50ed650a82f272ba128a1f872cda4d/sphinx/domains/std.py#L812-L816
        for objtype in objtypes:
            if (objtype, target) in domain.objects:
                docname, labelid = domain.objects[objtype, target]
                break
    return docname, labelid


def get_ref_numref_data(domain, node, typ, target):
    """
    Use Sphinx's internals to resolve :numref: and returns this data.

    :returns: tuple (``docname``, ``labelid``)
    """
    # Borrowed from https://github.com/sphinx-doc/sphinx/blob/47cd262b3e50ed650a82f272ba128a1f872cda4d/sphinx/domains/std.py#L699-L702
    if sphinx.version_info < (2, 1):
        if node['refexplicit']:
            docname, labelid = domain.data['anonlabels'].get(target, ('', ''))
        else:
            # reference to named label; the final node will
            # contain the section name after the label
            docname, labelid, sectname = domain.data['labels'].get(target, ('', '', ''))
    else:
        if target in domain.labels:
            docname, labelid, figname = domain.labels.get(target, ('', '', ''))
        else:
            docname, labelid = domain.anonlabels.get(target, ('', ''))
    return docname, labelid
