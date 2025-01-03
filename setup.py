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

author = ["Trevor Bača", "Joséphine Oberholtzer"]

author_email = [
    "trevor.baca@gmail.com",
    "josiah.oberholtzer@gmail.com",
]

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Artistic Software",
]

extras_require = {
    "nauert": ["abjad-ext-nauert>=3.19"],
    "rmakers": ["abjad-ext-rmakers>=3.19"],
    "dev": [
        "black>=23.7.0",
        "flake8>=6.1.0",
        "isort>=5.12.0",
        "mypy>=1.4.1",
        "pytest>=8.1.1",
        "pytest-cov>=4.1.0",
        "pytest-helpers-namespace>=2021.12.29",
        "sphinx-autodoc-typehints>=1.22.0",
        "sphinx-rtd-theme>=1.0.0",
    ],
}

keywords = [
    "music composition",
    "music notation",
    "lilypond",
]

install_requires = [
    "ply>=3.11",
    "roman>=1.4",
    "uqbar>=0.6.9",
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
        python_requires=">=3.10",
        url="https://abjad.github.io",
        version=version,
    )
