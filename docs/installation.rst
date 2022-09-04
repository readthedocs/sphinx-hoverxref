Installation
============

Install the package

.. tabs::

   .. tab:: from PyPI

      .. prompt:: bash

         pip install sphinx-hoverxref

   .. tab:: from GitHub

      .. prompt:: bash

         pip install git+https://github.com/readthedocs/sphinx-hoverxref


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
you can use ``:hoverxref:`` role to show a tooltip [#]_ when hovering with the mouse.

.. warning::

   This extension **requires a backend server** to retrieve the tooltip content.
   Currently, only `Read the Docs`_ is supported as backend server.
   Take into account that your documentation has to be hosted on Read the Docs for this extension to work.

If you prefer to apply this behavior to *all* your ``:ref:`` in your documentation,
you can use the config :confval:`hoverxref_auto_ref`.

See :ref:`usage:usage` for more use cases and :ref:`configuration:configuration` for a full list of available configs.


.. _Read the Docs: https://readthedocs.org/

.. [#] we use tooltips as a generic word, but we refer to both, tooltips and modal dialogues
