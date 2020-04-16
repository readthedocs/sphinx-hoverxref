# conf.py to run tests

master_doc = 'index'
extensions = [
    'sphinx.ext.autosectionlabel',
    'hoverxref.extension',
]

latex_documents = [
    (master_doc, 'test.tex', u'test Documentation',
     u'test', 'manual'),
]
