#! /usr/bin/env python
import os
import sys

import setuptools

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================

This version of Abjad requires Python {}.{}, but you're trying to
install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install abjad

This will install the latest version of Abjad which works on your
version of Python.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

version_file_path = os.path.join(os.path.dirname(__file__), "abjad", "_version.py")
with open(version_file_path, "r") as file_pointer:
    file_contents_string = file_pointer.read()
local_dict: dict = {}
exec(file_contents_string, None, local_dict)
__version__ = local_dict["__version__"]

description = "Abjad is a Python API for Formalized Score Control."

with open("README.rst", "r") as file_pointer:
    long_description = file_pointer.read()

author = ["Trevor Bača", "Josiah Wolf Oberholtzer", "Víctor Adán"]

author_email = [
    "trevor.baca@gmail.com",
    "josiah.oberholtzer@gmail.com",
    "contact@victoradan.net",
]

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Artistic Software",
]

# TODO: can this be removed?
entry_points = {"console_scripts": ["ajv = abjad.cli:run_ajv"]}

extras_require = {
    "cli": ["abjad-ext-cli>=3.1.0, <3.2.0"],
    "ipython": ["abjad-ext-ipython>=3.1.0, <3.2.0"],
    "nauert": ["abjad-ext-nauert>=3.1.0, <3.2.0"],
    "rmakers": ["abjad-ext-rmakers>=3.1.0, <3.2.0"],
    "tonality": ["abjad-ext-tonality>=3.1.0, <3.2.0"],
    "test": [
        "black",
        "flake8",
        "isort",
        "mypy>=0.770",
        "pytest>=5.4.3",
        "pytest-cov>=2.7.1",
        "pytest-helpers-namespace",
    ],
}

keywords = [
    "music composition",
    "music notation",
    "formalized score control",
    "lilypond",
]

install_requires = ["ply", "quicktions>=1.3", "roman", "uqbar>=0.4.4, <0.5.0"]

if __name__ == "__main__":
    setuptools.setup(
        author=", ".join(author),
        author_email=", ".join(author_email),
        classifiers=classifiers,
        description=description,
        entry_points=entry_points,
        extras_require=extras_require,
        include_package_data=True,
        install_requires=install_requires,
        keywords=", ".join(keywords),
        license="MIT",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        name="Abjad",
        packages=["abjad"],
        platforms="Any",
        url="https://abjad.github.io",
        version=__version__,
    )
