Usage
=====

This extension defines a custom role called ``:hoverxref:``.
When this role is used, it will show a tooltip when ``hover`` mouse event is triggered,
and will populate the content tooltip with the content of the document and section the link is pointing to.

``:hoverxref:`` uses Sphinx's internals reference resolution to find out where the link points to.
So, the way of referencing the section works in the same way as the ``:ref:`` standard role.

Simplest usage example,

.. code-block:: rst

   This will :hoverxref:`show a tooltip <hoverxref:section>` in the linked words to ``hoverxref``.


Tooltip on custom object
------------------------

Sphinx has the ability to define custom objects via `Sphinx.add_object_type`_.
``hoverxref`` can also show a tooltip on these objects if desired.
To do that, when calling ``add_object_type`` you have to pass a specific function to ``parse_node`` argument.
Let's say that we want to define a custom role and directive called ``confval``.
In this case, calling ``Sphinx.add_object_type`` will look like:

.. code-block:: python
   :emphasize-lines: 9

   def setup(app):
       # ...
       from hoverxref.nodeparser import parse_node
       app.add_object_type(
           'confval',  # directivename
           'confval',  # rolename
           'pair: %s; configuration value',  # indextemplate
           parse_node=parse_node('confval'),
       )

Once object is added, ``hoverxref`` will know that we want to add tooltips on these objects.

Example
~~~~~~~

This documentation defines the ``confval`` role as described above.
The role is used to define all the configurations of the extension.
These configurations are added to the Sphinx index and we can easily refer to them and show a tooltip.
This is reStructuredText code to do this:

.. code-block:: rst

   This will show a tooltip to :confval:`hoverxref_auto_ref <configuration:confval-hoverxref_auto_ref>` configuration.

the previous code will render to:

This will show a tooltip to :confval:`hoverxref_auto_ref <configuration:confval-hoverxref_auto_ref>` configuration.


.. _Sphinx.add_object_type: https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_object_type
