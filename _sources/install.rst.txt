Installation
------------


You must have a Google Earth Engine account. If you don't yet have an account, you can request for it `here <http://signup.earthengine.google.com/#!/>`_ 

Once you have an account, the package can be installed using ``pip``, preferably within a virtual environment. If you're new to python and/or virtual environments, read the :ref:`scratch` section.


.. code-block:: bash

    pip install geextract

If you're using the gee API for the first time on your machine, you'll have to run:

.. code-block:: bash

	earthengine authenticate

which will open a google authentication page in your browser, and will give you an authentication token to paste back in the terminal.

You can check that the authentication process was successful by running.

.. code-block:: bash

    python -c "import ee; ee.Initialize()"


If nothing happens, it means that things are working... You can go ahead and use the ``geextract`` API and command line.


.. _scratch:

Install from scratch
--------------------

This section details step by step installation and setup from scratch. It includes installating and seting up `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ on ubuntu/debian. For windows and mac, refer to the `gee API installation instructions <https://developers.google.com/earth-engine/python_install_manual>`_.

Install dependencies
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Install pip (a package manager for python)
    sudo apt-get install python-pip

    # Install virtualenv (virtual environments for python projects)
    sudo pip install virtualenv

    # Install virtualenvwrapper (Makes working with virtualenv easier)
    sudo pip install virtualenvwrapper

    # Finish setting up virtualenvwraper (of course if you use a different shell, export to the right config file)
    echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
    source ~/.bashrc

    # Create a virtual environement
    mkvirtualenv geextract

    # You are now in the virtual environment
    # You can exit it by running 'deactivate'
    # And get back to it with 'workon geextract'

Install the package
^^^^^^^^^^^^^^^^^^^

To install the ``geextract`` package, run the following line in your terminal from within a virtual environment.

.. code-block:: bash

    # Install
    pip install geextract

You then need to authenticate for the package to be able to interact with the Google Earth Engine platform.

.. code-block:: bash

	earthengine authenticate

which will open a google authentication page in your browser, and will give you an authentication token to paste back in the terminal.

You can check that the authentication process was successful by running.

.. code-block:: bash

    python -c "import ee; ee.Initialize()"


If nothing happens, it means that things are working... You can go ahead and use the ``geextract`` API and command line.