Installation
============

Install the package

.. tabs::

   .. tab:: from GitHub

      .. prompt:: bash

         pip install git+https://github.com/humitos/sphinx-hoverxref@master


Once we have the package installed,
we have to configure it on our Sphinx documentation.
To do this, add this extension to your Sphinx's extensions in the ``conf.py`` file.

.. code-block:: python

   # conf.py
   extensions = [
        # ... other extensions here
        'hoverxref.extension',
   ]


After installing the package and adding the extension in the ``conf.py`` file,
all the ``:ref:`` roles will show a tooltip when hovering with the mouse.
