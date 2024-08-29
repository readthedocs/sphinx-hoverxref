import inspect
import pytest
from unittest import mock

from sphinx.events import EventListener
from sphinx.ext.intersphinx._resolve import missing_reference as intersphinx_missing_reference
from hoverxref.extension import missing_reference

from .utils import srcdir


@pytest.mark.sphinx(
    srcdir=srcdir,
    buildername='latex',
    confoverrides={
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

    app.build()
    path = app.outdir / 'test.tex'
    assert path.exists() is True
    content = open(path).read()

    assert app.builder.format == 'latex'


@pytest.mark.sphinx(
    srcdir=srcdir,
    confoverrides={
        'hoverxref_domains': ['py'],
        'hoverxref_intersphinx': ['python'],
        'hoverxref_auto_ref': True,
        'extensions': [
            'sphinx.ext.intersphinx',
            'hoverxref.extension',
        ],
    },
)
def test_disconnect_intersphinx_listener(app, status, warning):
    """The ``missing-reference`` listener from ``sphinx.ext.intershinx`` should be dropped in favor of ours."""
    app.build()
    missing_reference_listeners = app.events.listeners['missing-reference']
    assert EventListener(id=mock.ANY, priority=mock.ANY, handler=intersphinx_missing_reference) not in missing_reference_listeners
    assert EventListener(id=mock.ANY, priority=mock.ANY, handler=missing_reference) in missing_reference_listeners
