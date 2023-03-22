Releasing a new version
=======================

This project uses `flit <https://flit.pypa.io/en/latest/>`_  and `bumpver <https://github.com/mbarkhau/bumpver>`_ for this process.
These are the steps needed to release a new version:

#. Install the dependencies::

     $ pip install flit bumpver

#. Update the ``CHANGELOG.rst`` with the changes included in this release
#. Add ``CHANGELOG.rst`` to git stage::

     $ git add CHANGELOG.rst

#. Increase version (``--patch``, ``--minor`` or ``--major``)::

     $ bumpver update --minor --allow-dirty

#. Build the package and check everything is correct::

     $ rm -rf dist/ build/
     $ flit build

#. Upload the package to PyPI::

     $ flit publish
