Releasing a new version
=======================

These are the steps needed to release a new version:

#. Increment the version in ``hoverxerf/__init__.py``
#. Update the ``CHANGELOG.rst``
#. Commit the changes: ``git commit -m "Release $NEW_VERSION"``
#. Tag the release in git: ``git tag $NEW_VERSION``
#. Push the tag to GitHub: ``git push --tags origin``
#. Upload the package to PyPI::

     $ rm -rf dist/ build/
     $ pip install twine build
     $ python -m build --wheel --sdist
     $ twine upload dist/*
