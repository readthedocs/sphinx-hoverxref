import inspect
import pytest

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
    """Confirm that disconnecting the ``missing-reference`` listener from ``sphinx.ext.intershinx`` is successful."""
    app.build()
    listeners = []
    for listener in app.events.listeners.get('missing-reference'):
        module_name = inspect.getmodule(listener.handler).__name__
        if module_name.startswith('sphinx.ext.intersphinx'):
            listeners.append((module_name, listener))
    assert not listeners, f"Expected to find zero listeners but found: {listeners}"
