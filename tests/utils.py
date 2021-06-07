import os


srcdir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'examples',
    'default',
)

# srcdir with ``autosectionlabel_prefix_document = True`` config
prefixdocumentsrcdir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'examples',
    'prefixdocument',
)

# srcdir with ``Sphinx.add_object_type`` call
customobjectsrcdir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'examples',
    'custom-object',
)

# srcdir with ``:py:class:`` call
pythondomainsrcdir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'examples',
    'python-domain',
)

# srcdir with intersphinx configured
intersphinxsrc = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'examples',
    'intersphinx',
)
