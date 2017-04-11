# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('trail/trail.py').read(),
    re.M
).group(1)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name='trail',
    packages=['trail'],  # this must be the same as the name above
    entry_points={
        "console_scripts": ['trail = trail.trail:main']
    },
    version=version,
    description='Keep track of your thoughts.',
    long_description=long_descr,
    author='tolbot',
    author_email='eltolis@hotmail.com',
    url='https://github.com/tolbot/trail',  # use the URL to the github repo
    download_url='https://github.com/tolbot/trail/archive/{}.tar.gz'.format(version),  # make sure proper github tags are added; see below
    keywords=['todo', 'productivity', 'notes'],  # arbitrary keywords
    classifiers=[],
)

# git tag 0.1 -m "Adds a tag so that we can put this on PyPI."
# git push --tags origin master
