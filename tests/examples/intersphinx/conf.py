# conf.py to run tests

master_doc = 'index'
extensions = [
    'hoverxref.extension',
    'sphinx.ext.intersphinx',
]

autosectionlabel_prefix_document = True

# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
intersphinx_cache_limit = -1
