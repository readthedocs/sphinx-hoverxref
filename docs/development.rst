Development
===========

This is a very small guide to help with the development of this extension.
Since it needs a backend and the event is only triggered only on mouse hover,
it could be tedious if you don't know these tips & tricks.

Backend
-------

This extension needs a Read the Docs backend to retrieve the content that will be inserted in the tooltip.
You can use the API from https://readthedocs.org directly or a local instance of Read the Docs as backend.

Using readthedocs.org as backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the easiest way to have the backend working, since you do not need to do anything.
Although, you need to use an already existent project in Read the Docs.

To setup this approach, you need to put these settings in the ``conf.py`` of your docs:

.. code-block:: python

   hoverxref_api_host = 'https://readthedocs.org'

After building the documentation all the requests will be done to URLs like::

  https://readthedocs.org/api/v3/embed/?doctool=sphinx&doctoolversion=...&url=...

.. note::

   The project *and* version has to be successfully built on Read the Docs to return the content requested.


Building and serving docs locally
+++++++++++++++++++++++++++++++++

With your documentation's project configured with the previous settings,
you are ready to build and serve the docs from your computer.

Build the documentation with these commands:

.. prompt:: bash

   cd docs/
   make clean
   make html

Serve the documentation locally with this command:

.. prompt:: bash

   python -m http.server --directory _build/html 9000

Now, you can hit http://localhost:9000/ and you should see your documentation here.


Avoid CORS on local backend
+++++++++++++++++++++++++++

When building the documentation locally,
the API calls will be blocked by the browser because of :abbr:`CORS (Cross Origin Resource Sharing)`
(you are hitting the URL http://localhost:9000/ and the API calls are to https://readthedocs.org/).

You can disable this while developing our extension.
To do this, you can open Google Chrome with these arguments:

.. prompt:: bash

   google-chrome-stable --disable-web-security --user-data-dir='/tmp/testing'

If Firefox, you can install this add-ons: `Allow CORS: Access-Control-Allow-Origin <https://addons.mozilla.org/es/firefox/addon/access-control-allow-origin/>`_.


Using a local Read the Docs instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can `install Read the Docs locally following these instructions`_.
Although, it may be too complicated just to retrieve the same content that you could have in https://readthedocs.org.

To make the extension to work, you will need to define this setting in your ``conf.py`` file:

.. code-block:: python

   hoverxref_api_host = 'http://community.dev.readthedocs.io'

.. tip::

   The value of this setting should be the same as ``PUBLIC_API_URL``.

Once you have done that, you can just import the project directly in your local instance,
and the tooltips should work without problem.

.. _install Read the Docs locally following these instructions: https://docs.readthedocs.io/en/stable/development/install.html


Permanent tooltip to work with CSS
----------------------------------

You need to find the selector of the ``a`` element that you want to emulate the *mouse hover* event first,
then from the Javascript console, you can force the browser to trigger this event for us.
This way, the element is inserted in the DOM and will persist there.
Now, you can find the ``div`` for the tooltipster and edit the CSS used to render it.

.. code-block:: javascript

   $('#section > p > a').trigger('mouseenter')


Happy hacking!
