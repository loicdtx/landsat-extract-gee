Installation
------------

You must have a Google Earth Engine account. If you don't yet have an account, you can request for it ..`here`_ 

.. _here: https://signup.earthengine.google.com/#!/

.. code-block:: bash

    pip install git+https://github.com/loicdtx/landsat-extract-gee.git

If you're using the gee API for the first time on your machine, you'll have to run:

.. code-block:: bash

	earthengine authenticate

which will open a google authentication page in your browser, and will give you an authentication token to paste back in the terminal.

You can check that the authentication process was successful by running.

.. code-block:: bash

    python -c "import ee; ee.Initialize()"


If nothing happens, it means that things are working...