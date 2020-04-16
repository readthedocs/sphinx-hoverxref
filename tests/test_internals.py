import inspect
import os
import pytest
import shutil

from hoverxref.translators import HoverXRefHTMLTranslatorMixin

from .utils import srcdir


@pytest.mark.sphinx(
    srcdir=srcdir,
    buildername='latex',
    confoverrides={
        'hoverxref_project': 'myproject',
        'hoverxref_version': 'myversion',
    },
)
def test_dont_override_translator_non_html_builder(app, status, warning):
    app.build()
    path = app.outdir / 'python.tex'
    assert path.exists() is True
    content = open(path).read()

    assert app.builder.format == 'latex'
    for name, klass in app.registry.translators.items():
        assert not issubclass(klass, HoverXRefHTMLTranslatorMixin)


@pytest.mark.sphinx(
    srcdir=srcdir,
    buildername='html',
    confoverrides={
        'hoverxref_project': 'myproject',
        'hoverxref_version': 'myversion',
    },
)
def test_override_translator_non_html_builder(app, status, warning):
    app.build()
    path = app.outdir / 'index.html'
    assert path.exists() is True
    content = open(path).read()

    assert app.builder.format == 'html'
    for name, klass in app.registry.translators.items():
        assert issubclass(klass, HoverXRefHTMLTranslatorMixin)
