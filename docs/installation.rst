Installation
============

Install the package

.. tabs::

   .. tab:: from PyPI

      .. prompt:: bash

         pip install --pre sphinx-hoverxref

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
you can use ``:hoverxref:`` role to show tooltip when hovering with the mouse.

If you prefer to apply this behavior to *all* your ``:ref:`` in your documentation,
you can use the config :confval:`hoverxref_auto_ref`.

See :ref:`usage:usage` for more use cases and :ref:`configuration:configuration` for a full list of available configs.
