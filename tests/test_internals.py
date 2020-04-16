import inspect
import os
import pytest
import shutil
from unittest import mock

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
    path = app.outdir / 'test.tex'
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


@pytest.mark.sphinx(
    srcdir=srcdir,
    buildername='latex',
    confoverrides={
        'hoverxref_project': 'myproject',
        'hoverxref_version': 'myversion',
        'hoverxref_auto_ref': True,
    },
)
def test_dont_fail_non_html_builder(app, status, warning):
    """
    Test our resolver is not used by non-HTML builder.

    When running the build with ``latex`` as builder and
    ``hoverxref_auto_ref=True`` it should not fail with

    def _get_docpath(self, builder, docname):
        docpath = builder.get_outfilename(docname)
        AttributeError: 'LaTeXBuilder' object has no attribute 'get_outfilename'

    LaTeXBuilder should never use our resolver.
    """

    with mock.patch('hoverxref.domains.HoverXRefBaseDomain._get_docpath') as _get_docpath:
        app.build()
        assert not _get_docpath.called
    path = app.outdir / 'test.tex'
    assert path.exists() is True
    content = open(path).read()

    assert app.builder.format == 'latex'
