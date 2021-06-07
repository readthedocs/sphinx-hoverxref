import os
import shutil
import pytest

from .utils import srcdir, prefixdocumentsrcdir, customobjectsrcdir, pythondomainsrcdir, intersphinxsrc


@pytest.fixture(autouse=True, scope='function')
def remove_sphinx_build_output():
    """Remove _build/ folder, if exist."""
    for path in (srcdir, prefixdocumentsrcdir, customobjectsrcdir, pythondomainsrcdir, intersphinxsrc):
        build_path = os.path.join(path, '_build')
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
