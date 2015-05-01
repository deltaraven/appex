
### Python Example Application Using py2app

A simple application demonstrating an app which uses `py2app` to generate a Mac
OS X `.app` bundle. All package requirements may be found in the
`requirements.txt` file.

---
### Setup Development Environment

**Make a virtual environment**

Using `virtualenvwrapper` here, so this section may differ depending on your
virtualenv setup.

``` sh
mkvirtualenv appex
```

**Link the PostgreSQL executables**

The following step must be done before (re)installing `psycopg2`.

``` sh
ln -fs </path/to/your/postgresql>/bin/* $VIRTUAL_ENV/bin/
```

**Install packages**

``` sh
cd </path/to/appex>
pip install -r requirements.txt
```

---
### Build Mac OS X .app bundle

After executing the following command, the app bundle will be placed in the
`./dist` directory.

``` sh
python setup.py py2app
```
