import os
import pytest


srcdir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'examples',
    'default',
)


@pytest.mark.sphinx(
    srcdir=srcdir,
)
def test_default_settings(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() == True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" href="chapter-i.html#chapter-i"><span class="std std-ref">This a reference to Chapter I</span></a>',
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
    assert path.exists() == True
    content = open(path).read()

    chunks = [
        '<a class="reference internal" data-doc="index" data-project="myproject" data-section="chapter i" data-version="myversion" href="chapter-i.html#chapter-i"><span class="std std-ref">This a reference to Chapter I</span></a>',
    ]

    for chunk in chunks:
        assert chunk in content
