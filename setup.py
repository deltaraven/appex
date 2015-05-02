
LICENSE = """Copyright (c) 2015, Joel Miller <joel@deltaraven.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

from setuptools import setup, find_packages

setup(
    name='appex',
    version="0.1",
    description="python py2app example application",
    author="Joel Miller",
    author_email="joel@deltaraven.com",
    license=LICENSE,
    packages=find_packages(),
    app = ["appex.py"],
    setup_requires=["py2app"],
    options = {
        "py2app": { "argv_emulation": True },
    },
    install_requires=[
        "SQLAlchemy",
        "psycopg2",
    ],
    entry_points = {
        "console_scripts": ["appex = appex:main"],
    }
)
