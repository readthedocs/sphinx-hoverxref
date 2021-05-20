# conf.py to run tests

master_doc = 'index'
extensions = [
    'sphinx.ext.intersphinx',
    'hoverxref.extension',  # NOTE: this order is important
]

hoverxref_intersphinx = True
hoverxref_intersphinx_type = 'modal'
autosectionlabel_prefix_document = True

# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
intersphinx_cache_limit = 0