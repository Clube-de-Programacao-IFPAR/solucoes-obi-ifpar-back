.. solucoes-obi-ifpar documentation master file, created by
   sphinx-quickstart on Sat Apr  4 14:39:50 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

solucoes-obi-ifpar documentation
================================

Welcome to the repository docs!

This will mostly document the api
used in this project to manage what will be a growing amount of
endpoints in the future.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

How to build the docs
---------------------

1. Install the Sphinx dependencies at docs/requirements.txt and the project
dependencies at src/requirements.txt with pip:

.. code-block:: console

   $ pip install -r docs/requirements.txt -r src/requirements.txt

2. ``cd`` to src and run ``rm -r ../docs/build/html && sphinx-build ../docs/source/ ../docs/build/html/``:

.. code-block:: console

   $ cd src
   $ rm -r ../docs/build/html & sphinx-build ../docs/source/ ../docs/build/html/

3. The docs will be avaliable at ``docs/build/html``, use your prefered browser to access the page at ``docs/build/html/index.html``.