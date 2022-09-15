import pytest

from .utils import srcdir


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
        'hoverxref_tooltip_lazy': True,
    },
)
def test_lazy_tooltips(app, status, warning):
    app.build()
    path = app.outdir / '_static/js/hoverxref.js'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        ".one('mouseenter click touchstart tap', function(event) {",
        ".tooltipster('open');",
    ]

    for chunk in chunks:
        assert chunk in content

    ignored_chunks = [
        ".each(function () { $(this).removeAttr('title') });",
    ]
    for chunk in ignored_chunks:
        assert chunk not in content


@pytest.mark.sphinx(
    srcdir=srcdir,
)
def test_lazy_tooltips_notlazy(app, status, warning):
    app.build()
    path = app.outdir / '_static/js/hoverxref.js'
    assert path.exists() is True
    content = open(path).read()

    chunks = [
        ".each(function () { $(this).removeAttr('title') });",
    ]

    for chunk in chunks:
        assert chunk in content

    ignored_chunks = [
        ".one('mouseenter click touchstart tap', function(event) {",
        ".tooltipster('open');",
    ]
    for chunk in ignored_chunks:
        assert chunk not in content
