# conf.py to run tests

master_doc = 'index'
extensions = [
    'sphinx.ext.autosectionlabel',
    'hoverxref.extension',
]

hoverxref_project = 'myproject'
hoverxref_version = 'myversion'


def setup(app):
    from hoverxref.parser import parse_node
    app.add_object_type(
        'confval',  # directivename
        'confval',  # rolename
        'pair: %s; configuration value',  # indextemplate
        parse_node=parse_node('confval'),
    )
