# conf.py to run tests

master_doc = 'index'
extensions = [
    'sphinx.ext.autosectionlabel',
    'hoverxref.extension',
]

hoverxref_roles = [
    'confval',
    'numref',
]

numfig = True

def setup(app):
    app.add_object_type(
        'confval',  # directivename
        'confval',  # rolename
        'pair: %s; configuration value',  # indextemplate
    )
