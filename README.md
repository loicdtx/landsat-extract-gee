

## Installation

In vitual environment

```
pip install git+https://github.com/loicdtx/landsat-extract-gee.git
```

If you're using the gee API for the first time on your machine, you'll have to run:

```
earthengine authenticate
```

which will open a google authentication page in your browser, and will give you an authentication token to paste back in the terminal.

You can check that the authentication process was successful by running.

```
python -c "import ee; ee.Initialize()"
```

If nothing happens... it's working.

