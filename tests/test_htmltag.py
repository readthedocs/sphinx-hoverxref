import pytest
import sphinx
import textwrap

from .utils import srcdir, prefixdocumentsrcdir, customobjectsrcdir, pythondomainsrcdir, intersphinxsrc


@pytest.mark.sphinx(
    srcdir=srcdir,
)
def test_default_settings(app, status, warning):
    """The extension should not change the output if not configured."""
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :ref: to Chapter I</span></a>',
        '<a class="reference internal" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
        'hoverxref_project': 'myproject',
        'hoverxref_version': 'myversion',
    },
)
def test_project_version_settings(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :ref: to Chapter I</span></a>',
        '<a class="hoverxref tooltip reference internal" data-doc="chapter-i" data-docpath="/chapter-i.html" data-project="myproject" data-section="section-i" data-version="myversion" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
        'hoverxref_project': 'myproject',
        'hoverxref_version': 'myversion',
    },
)
def test_js_render(app, status, warning):
    app.build()
    path = app.outdir / '_static' / 'js' / 'hoverxref.js'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        "theme: ['tooltipster-shadow', 'tooltipster-shadow-custom']",
        "interactive: true",
        "maxWidth: 450",
        "animation: 'fade'",
        "animationDuration: 0",
        "content: 'Loading...'",
        "var url = 'https://readthedocs.org' + '/api/v2/embed/?' + $.param(params);",
        textwrap.indent(textwrap.dedent("""
        var params = {
                'project': project,
                'version': version,
                'doc': doc,
                'path': docpath,
                'section': section,
            }"""), '    ').strip(),
        textwrap.indent(textwrap.dedent("""
        var params = {
                'url': url,
            }"""), '    ').strip(),
        "var sphinxtabs = false",
        "var mathjax = false",
        "var url = $origin.data('url');",
        "var url = getEmbedURL(project, version, doc, docpath, section, url);",
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=prefixdocumentsrcdir,
    confoverrides={
        'hoverxref_project': 'myproject',
        'hoverxref_version': 'myversion',
    },
)
def test_autosectionlabel_project_version_settings(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :ref: to Chapter I</span></a>.',
        '<a class="hoverxref tooltip reference internal" data-doc="chapter-i" data-docpath="/chapter-i.html" data-project="myproject" data-section="chapter-i" data-version="myversion" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :hoverxref: to Chapter I</span></a>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=customobjectsrcdir,
    confoverrides={},
)
def test_custom_object(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="hoverxref tooltip reference internal" data-doc="configuration" data-docpath="/configuration.html" data-project="myproject" data-section="confval-conf-title" data-version="myversion" href="configuration.html#confval-conf-title"><code class="xref std std-confval docutils literal notranslate"><span class="pre">This</span> <span class="pre">is</span> <span class="pre">a</span> <span class="pre">:confval:</span> <span class="pre">to</span> <span class="pre">conf-title</span></code></a>',
        '<a class="hoverxref tooltip reference internal" data-doc="configuration" data-docpath="/configuration.html" data-project="myproject" data-section="configuration" data-version="myversion" href="configuration.html#configuration"><span class="std std-ref">This is a :hoverxref: to Configuration document</span></a>',
        '<a class="hoverxref tooltip reference internal" data-doc="code" data-docpath="/code.html" data-project="myproject" data-section="python-code-block" data-version="myversion" href="code.html#python-code-block"><span class="std std-numref">This is a :numref: to a Python code block (PyExample)</span></a>'
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=pythondomainsrcdir,
    confoverrides={
        'hoverxref_domains': ['py'],
    },
)
def test_python_domain(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="hoverxref tooltip reference internal" data-doc="api" data-docpath="/api.html" data-project="myproject" data-section="hoverxref.extension.HoverXRefStandardDomainMixin" data-version="myversion" href="api.html#hoverxref.extension.HoverXRefStandardDomainMixin" title="hoverxref.extension.HoverXRefStandardDomainMixin"><code class="xref py py-class docutils literal notranslate"><span class="pre">This</span> <span class="pre">is</span> <span class="pre">a</span> <span class="pre">:py:class:</span> <span class="pre">role</span> <span class="pre">to</span> <span class="pre">a</span> <span class="pre">Python</span> <span class="pre">object</span></code></a>',
        '<a class="hoverxref tooltip reference internal" data-doc="api" data-docpath="/api.html" data-project="myproject" data-section="hoverxref.extension" data-version="myversion" href="api.html#module-hoverxref.extension" title="hoverxref.extension"><code class="xref py py-mod docutils literal notranslate"><span class="pre">hoverxref.extension</span></code></a>',
        '<a class="hoverxref tooltip reference internal" data-doc="api" data-docpath="/api.html" data-project="myproject" data-section="hoverxref.utils.get_ref_xref_data" data-version="myversion" href="api.html#hoverxref.utils.get_ref_xref_data" title="hoverxref.utils.get_ref_xref_data"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.utils.get_ref_xref_data()</span></code></a>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
        'hoverxref_project': 'myproject',
        'hoverxref_version': 'myversion',
        'hoverxref_default_type': 'modal',
    },
)
def test_default_type(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :ref: to Chapter I</span></a>',
        '<a class="hoverxref modal reference internal" data-doc="chapter-i" data-docpath="/chapter-i.html" data-project="myproject" data-section="section-i" data-version="myversion" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
        'hoverxref_ignore_refs': [
            'section i',
        ],
    },
)
def test_ignore_refs(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :ref: to Chapter I</span></a>',
        '<a class="reference internal" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
    ]

    for chunk in chunks:
        assert chunk in content

    ignored_chunks = [
        '<a class="hoverxref reference internal" data-doc="chapter-i" data-project="myproject" data-section="section-i" data-version="myversion" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
    ]
    for chunk in ignored_chunks:
        assert chunk not in content


@pytest.mark.sphinx(
    srcdir=intersphinxsrc,
)
def test_intersphinx_default_configs(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="reference external" href="https://docs.python.org/3/tutorial/index.html#tutorial-index" title="(in Python v3.9)"><span class="xref std std-ref">This a :ref: to The Python Tutorial using intersphinx</span></a>',
        '<a class="reference external" href="https://docs.python.org/3/library/datetime.html#datetime-datetime" title="(in Python v3.9)"><span class="xref std std-ref">This a :ref: to datetime.datetime Python’s function using intersphinx</span></a>',
        '<a class="reference external" href="https://docs.readthedocs.io/en/stable/config-file/v2.html#python" title="(in Read the Docs v5.17.0)"><span class="xref std std-ref">This a :ref: to Config File v2 Read the Docs’ page using intersphinx</span></a>',
        '<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.9)"><code class="xref py py-class docutils literal notranslate"><span class="pre">float</span></code></a>',
        '<a class="reference internal" href="#hoverxref.extension.setup" title="hoverxref.extension.setup"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.extension.setup()</span></code></a>',
    ]

    if sphinx.version_info >= (4, 0):
        chunks.extend([
            '<dt class="sig sig-object py" id="hoverxref.extension.setup">',
        ])
    else:
        chunks.extend([
            '<dt id="hoverxref.extension.setup">',
        ])


    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=intersphinxsrc,
    confoverrides={
        'hoverxref_intersphinx': [
            'python',
        ],
    },
)
def test_intersphinx_python_mapping(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        # Python's links do have hoverxref enabled
        '<a class="hoverxref tooltip reference external" data-url="https://docs.python.org/3/tutorial/index.html#tutorial-index" href="https://docs.python.org/3/tutorial/index.html#tutorial-index" title="(in Python v3.9)"><span class="xref std std-ref">This a :ref: to The Python Tutorial using intersphinx</span></a>',
        '<a class="hoverxref tooltip reference external" data-url="https://docs.python.org/3/library/datetime.html#datetime-datetime" href="https://docs.python.org/3/library/datetime.html#datetime-datetime" title="(in Python v3.9)"><span class="xref std std-ref">This a :ref: to datetime.datetime Python’s function using intersphinx</span></a>',
        '<a class="hoverxref tooltip reference external" data-url="https://docs.python.org/3/library/functions.html#float" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.9)"><code class="xref py py-class docutils literal notranslate"><span class="pre">float</span></code></a>',

        # Read the Docs' link does not have hoverxref enabled
        '<a class="reference external" href="https://docs.readthedocs.io/en/stable/config-file/v2.html#python" title="(in Read the Docs v5.17.0)"><span class="xref std std-ref">This a :ref: to Config File v2 Read the Docs’ page using intersphinx</span></a>',

        # Python's domain does not have hoverxref enabled
        '<a class="reference internal" href="#hoverxref.extension.setup" title="hoverxref.extension.setup"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.extension.setup()</span></code></a>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=intersphinxsrc,
    confoverrides={
        'hoverxref_intersphinx': [
            'readthedocs',
            'python',
        ],
        'hoverxref_intersphinx_types': {
            'readthedocs': 'modal',
            'python': {
                'class': 'modal',
            }
        },
        'hoverxref_domains': ['py'],
    },
)
def test_intersphinx_all_mappings(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        # Python's links do have hoverxref enabled
        '<a class="hoverxref tooltip reference external" data-url="https://docs.python.org/3/tutorial/index.html#tutorial-index" href="https://docs.python.org/3/tutorial/index.html#tutorial-index" title="(in Python v3.9)"><span class="xref std std-ref">This a :ref: to The Python Tutorial using intersphinx</span></a>',
        '<a class="hoverxref tooltip reference external" data-url="https://docs.python.org/3/library/datetime.html#datetime-datetime" href="https://docs.python.org/3/library/datetime.html#datetime-datetime" title="(in Python v3.9)"><span class="xref std std-ref">This a :ref: to datetime.datetime Python’s function using intersphinx</span></a>',
        '<a class="hoverxref modal reference external" data-url="https://docs.python.org/3/library/functions.html#float" href="https://docs.python.org/3/library/functions.html#float" title="(in Python v3.9)"><code class="xref py py-class docutils literal notranslate"><span class="pre">float</span></code></a>',

        # Read the Docs' link does have hoverxref enabled
        '<a class="hoverxref modal reference external" data-url="https://docs.readthedocs.io/en/stable/config-file/v2.html#python" href="https://docs.readthedocs.io/en/stable/config-file/v2.html#python" title="(in Read the Docs v5.17.0)"><span class="xref std std-ref">This a :ref: to Config File v2 Read the Docs’ page using intersphinx</span></a>',

        # Python domain's link does have hoverxref enabled
        '<a class="hoverxref tooltip reference internal" data-doc="index" data-docpath="/index.html" data-project="myproject" data-section="hoverxref.extension.setup" data-version="myversion" href="#hoverxref.extension.setup" title="hoverxref.extension.setup"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.extension.setup()</span></code></a>',
    ]

    for chunk in chunks:
        assert chunk in content
