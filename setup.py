
import os
import sys

from setuptools import setup, find_packages

setup(
    name='appex',
    version="0.1",
    description="python py2app example application",
    author="Joel Miller",
    author_email="joel@deltaraven.com",
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
