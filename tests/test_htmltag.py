import re
import pytest
import sphinx
import textwrap

from hoverxref import __version__

from .utils import srcdir, prefixdocumentsrcdir, customobjectsrcdir, pythondomainsrcdir, intersphinxsrc, bibtexdomainsrcdir


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
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=srcdir,
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
        "contentAsHTML: true",
        "content: 'Loading...'",
        "var url = 'https://readthedocs.org' + '/api/v3/embed/?' + $.param(params);",
        textwrap.indent(
            textwrap.dedent("""
            var params = {{
                'doctool': 'sphinx',
                'doctoolversion': '{}',
                'url': url,
            }}""".format(sphinx.__version__)),
            '    ',
        ).strip(),
        "var sphinxtabs = false",
        "var mathjax = false",
        "var url = getEmbedURL(href);",
        f"headers: {{'X-HoverXRef-Version': '{__version__}'}}",
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=prefixdocumentsrcdir,
)
def test_autosectionlabel_project_version_settings(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :ref: to Chapter I</span></a>.',
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a :hoverxref: to Chapter I</span></a>',
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
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="configuration.html#confval-conf-title"><code class="xref std std-confval docutils literal notranslate"><span class="pre">This</span> <span class="pre">is</span> <span class="pre">a</span> <span class="pre">:confval:</span> <span class="pre">to</span> <span class="pre">conf-title</span></code></a>',
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="configuration.html#configuration"><span class="std std-ref">This is a :hoverxref: to Configuration document</span></a>',
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="code.html#python-code-block"><span class="std std-numref">This is a :numref: to a Python code block (PyExample)</span></a>'
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
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="api.html#hoverxref.extension.HoverXRefStandardDomainMixin" title="hoverxref.extension.HoverXRefStandardDomainMixin"><code class="xref py py-class docutils literal notranslate"><span class="pre">This</span> <span class="pre">is</span> <span class="pre">a</span> <span class="pre">:py:class:</span> <span class="pre">role</span> <span class="pre">to</span> <span class="pre">a</span> <span class="pre">Python</span> <span class="pre">object</span></code></a>',
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="api.html#module-hoverxref.extension" title="hoverxref.extension"><code class="xref py py-mod docutils literal notranslate"><span class="pre">hoverxref.extension</span></code></a>',
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="api.html#hoverxref.extension.setup" title="hoverxref.extension.setup"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.extension.setup()</span></code></a>',
        '<code class="xref py py-const docutils literal notranslate"><span class="pre">Constant</span></code>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=pythondomainsrcdir,
    confoverrides={
        'hoverxref_domains': ['py'],
        'hoverxref_intersphinx': ['python'],
        'hoverxref_auto_ref': True,
        'extensions': [
            'sphinx.ext.autodoc',
            'sphinx.ext.autosectionlabel',
            'sphinx.ext.intersphinx',
            'hoverxref.extension',
        ],
    },
)
def test_python_domain_intersphinx(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="api.html#hoverxref.extension.HoverXRefStandardDomainMixin" title="hoverxref.extension.HoverXRefStandardDomainMixin"><code class="xref py py-class docutils literal notranslate"><span class="pre">This</span> <span class="pre">is</span> <span class="pre">a</span> <span class="pre">:py:class:</span> <span class="pre">role</span> <span class="pre">to</span> <span class="pre">a</span> <span class="pre">Python</span> <span class="pre">object</span></code></a>',
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="api.html#module-hoverxref.extension" title="hoverxref.extension"><code class="xref py py-mod docutils literal notranslate"><span class="pre">hoverxref.extension</span></code></a>',
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="api.html#hoverxref.extension.setup" title="hoverxref.extension.setup"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.extension.setup()</span></code></a>',
        '<code class="xref py py-const docutils literal notranslate"><span class="pre">Constant</span></code>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.skipif(
    sphinx.version_info < (2, 1, 0),
    reason='sphinxcontrib-bibtex requires Sphinx>=2.1 to work',
)
@pytest.mark.sphinx(
    srcdir=bibtexdomainsrcdir,
    confoverrides={
        'hoverxref_domains': ['cite'],
    },
)
def test_bibtex_domain(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<p>See <span id="id1">Nelson [<a class="hxr-hoverxref hxr-tooltip reference internal" href="#id4" title="Edward Nelson. Radically Elementary Probability Theory. Princeton University Press, 1987.">Nel87</a>]</span> for an introduction to non-standard analysis.\nNon-standard analysis is fun <span id="id2">[<a class="hxr-hoverxref hxr-tooltip reference internal" href="#id4" title="Edward Nelson. Radically Elementary Probability Theory. Princeton University Press, 1987.">Nel87</a>]</span>.</p>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
        'hoverxref_roles': ['term'],
    },
)
def test_glossary_term_domain(app, status, warning):
    app.build()
    path = app.outdir / 'glossary.html'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        '<p>See definition <a class="hxr-hoverxref hxr-tooltip reference internal" href="#term-builder"><span class="xref std std-term">builder</span></a> for more information.</p>',
    ]

    for chunk in chunks:
        assert chunk in content


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
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
        '<a class="hxr-hoverxref hxr-modal reference internal" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
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
        '<a class="hxr-hoverxref reference internal" href="chapter-i.html#section-i"><span class="std std-ref">This a :hoverxref: to Chapter I, Section I</span></a>',
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

    chunks_regex = [
        r'<a class="reference external" href="https://docs.python.org/3/tutorial/index.html#tutorial-index" title="\(in Python v3.\d\d?\)"><span class="xref std std-ref">This a :ref: to The Python Tutorial using intersphinx</span></a>',
        r'<a class="reference external" href="https://docs.python.org/3/library/datetime.html#datetime-datetime" title="\(in Python v3.\d\d?\)"><span class="xref std std-ref">This a :ref: to datetime.datetime Python’s function using intersphinx</span></a>',
        r'<a class="reference external" href="https://docs.readthedocs.io/en/stable/config-file/v2.html#python" title="\(in Read the Docs user documentation v\d\d?.\d\d?.\d\d?\)"><span class="xref std std-ref">This a :ref: to Config File v2 Read the Docs’ page using intersphinx</span></a>',
        r'<a class="reference external" href="https://docs.python.org/3/library/functions.html#float" title="\(in Python v3.\d\d?\)"><code class="xref py py-class docutils literal notranslate"><span class="pre">float</span></code></a>',
    ]

    chunks = [
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

    for chunk in chunks_regex:
        assert re.search(chunk, content)


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

    chunks_regex = [
        # Python's links do have hoverxref enabled
        r'<a class="hxr-hoverxref hxr-tooltip reference external" href="https://docs.python.org/3/tutorial/index.html#tutorial-index" title="\(in Python v3.\d\d?\)"><span class="xref std std-ref">This a :ref: to The Python Tutorial using intersphinx</span></a>',
        r'<a class="hxr-hoverxref hxr-tooltip reference external" href="https://docs.python.org/3/library/datetime.html#datetime-datetime" title="\(in Python v3.\d\d?\)"><span class="xref std std-ref">This a :ref: to datetime.datetime Python’s function using intersphinx</span></a>',
        r'<a class="hxr-hoverxref hxr-tooltip reference external" href="https://docs.python.org/3/library/functions.html#float" title="\(in Python v3.\d\d?\)"><code class="xref py py-class docutils literal notranslate"><span class="pre">float</span></code></a>',

        # Read the Docs' link does not have hoverxref enabled
        r'<a class="reference external" href="https://docs.readthedocs.io/en/stable/config-file/v2.html#python" title="\(in Read the Docs user documentation v\d\d?.\d\d?.\d\d?\)"><span class="xref std std-ref">This a :ref: to Config File v2 Read the Docs’ page using intersphinx</span></a>',

    ]

    chunks = [
        # Python's domain does not have hoverxref enabled
        '<a class="reference internal" href="#hoverxref.extension.setup" title="hoverxref.extension.setup"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.extension.setup()</span></code></a>',
    ]

    for chunk in chunks:
        assert chunk in content

    for chunk in chunks_regex:
        assert re.search(chunk, content)


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
        'default_role': 'obj',
    },
)
def test_intersphinx_all_mappings(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    chunks_regex = [
        # Python's links do have hoverxref enabled
        r'<a class="hxr-hoverxref hxr-tooltip reference external" href="https://docs.python.org/3/tutorial/index.html#tutorial-index" title="\(in Python v3.\d\d?\)"><span class="xref std std-ref">This a :ref: to The Python Tutorial using intersphinx</span></a>',
        r'<a class="hxr-hoverxref hxr-tooltip reference external" href="https://docs.python.org/3/library/datetime.html#datetime-datetime" title="\(in Python v3.\d\d?\)"><span class="xref std std-ref">This a :ref: to datetime.datetime Python’s function using intersphinx</span></a>',
        r'<a class="hxr-hoverxref hxr-tooltip reference external" href="https://docs.python.org/3/library/datetime.html#datetime.time.minute" title="\(in Python v3.\d\d?\)"><code class="xref py py-attr docutils literal notranslate"><span class="pre">Python\'s</span> <span class="pre">datetime.time.minute</span></code></a>',
        r'<a class="hxr-hoverxref hxr-modal reference external" href="https://docs.python.org/3/library/functions.html#float" title="\(in Python v3.\d\d?\)"><code class="xref py py-class docutils literal notranslate"><span class="pre">float</span></code></a>',

        # Read the Docs' link does have hoverxref enabled
        r'<a class="hxr-hoverxref hxr-modal reference external" href="https://docs.readthedocs.io/en/stable/config-file/v2.html#python" title="\(in Read the Docs user documentation v\d\d?.\d\d?.\d+\)"><span class="xref std std-ref">This a :ref: to Config File v2 Read the Docs’ page using intersphinx</span></a>',

        # Using `default_role = 'obj'`
        # Note the difference with the same `float` line previouly. Here it uses `py-obj` instead of `py-class`.
        r'<a class="hxr-hoverxref hxr-tooltip reference external" href="https://docs.python.org/3/library/functions.html#float" title="\(in Python v3.\d\d?\)"><code class="xref py py-obj docutils literal notranslate"><span class="pre">float</span></code></a>'
    ]

    chunks = [
        # Python domain's link does have hoverxref enabled
        '<a class="hxr-hoverxref hxr-tooltip reference internal" href="#hoverxref.extension.setup" title="hoverxref.extension.setup"><code class="xref py py-func docutils literal notranslate"><span class="pre">hoverxref.extension.setup()</span></code></a>',
    ]

    for chunk in chunks:
        assert chunk in content

    for chunk in chunks_regex:
        assert re.search(chunk, content)
