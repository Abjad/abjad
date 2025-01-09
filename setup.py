#! /usr/bin/env python
import os

import setuptools


def get_abjad_version():
    version_file_path = os.path.join(os.path.dirname(__file__), "abjad", "_version.py")
    with open(version_file_path, "r") as file_pointer:
        file_contents_string = file_pointer.read()
    local_dict: dict = {}
    exec(file_contents_string, None, local_dict)
    __version__ = local_dict["__version__"]
    return __version__


description = "Abjad is a Python API for building LilyPond files."

with open("README.rst", "r") as file_pointer:
    long_description = file_pointer.read()

author = ["Trevor Bača", "Joséphine Wolf Oberholtzer"]

author_email = [
    "trevor.baca@gmail.com",
    "josephine.wolf.oberholtzer@gmail.com",
]

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Artistic Software",
]

extras_require = {
    "nauert": ["abjad-ext-nauert>=3.20"],
    "rmakers": ["abjad-ext-rmakers>=3.20"],
    "dev": [
        "black>=24.10.0",
        "flake8>=7.1.1",
        "isort>=5.13.2",
        "mypy>=1.14.1",
        "pytest>=8.3.4",
        "pytest-cov>=6.0.0",
        "pytest-helpers-namespace>=2021.12.29",
        "sphinx>=8.1.3",
        "sphinx-rtd-theme>=3.0.2",
    ],
}

keywords = [
    "music composition",
    "music notation",
    "lilypond",
]

install_requires = [
    "ply>=3.11",
    "roman>=4.2",
    "uqbar>=0.7.4",
]

if __name__ == "__main__":
    version = get_abjad_version()
    setuptools.setup(
        author=", ".join(author),
        author_email=", ".join(author_email),
        classifiers=classifiers,
        description=description,
        extras_require=extras_require,
        include_package_data=True,
        install_requires=install_requires,
        keywords=", ".join(keywords),
        license="MIT",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        name="abjad",
        packages=["abjad"],
        platforms="Any",
        python_requires=">=3.12",
        url="https://abjad.github.io",
        version=version,
    )
