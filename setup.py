#! /usr/bin/env python
import os
import sys

import setuptools


def get_abjad_version():
    version_file_path = os.path.join(os.path.dirname(__file__), "abjad", "_version.py")
    with open(version_file_path, "r") as file_pointer:
        file_contents_string = file_pointer.read()
    local_dict: dict = {}
    exec(file_contents_string, None, local_dict)
    __version__ = local_dict["__version__"]
    return __version__


def check_python_version(abjad_version):
    CURRENT_PYTHON = sys.version_info[:2]
    SUPPORTED_PYTHONS = [(3, 10), (3, 11)]
    if CURRENT_PYTHON not in SUPPORTED_PYTHONS:
        current_python = ".".join([str(_) for _ in CURRENT_PYTHON])
        supported_pythons = ", ".join([f"{_[0]}.{_[1]}" for _ in SUPPORTED_PYTHONS])
        string = f"This is Abjad {abjad_version},"
        string += f" which supports Python {supported_pythons}.\n"
        string += "\n"
        string += "But it looks like you're trying to install Abjad"
        string += f" with Python {current_python}."
        sys.stderr.write(string)
        sys.exit(1)


description = "Abjad is a Python API for building LilyPond files."

with open("README.rst", "r") as file_pointer:
    long_description = file_pointer.read()

author = ["Trevor Bača", "Josiah Wolf Oberholtzer"]

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
    "nauert": ["abjad-ext-nauert>=3.17"],
    "rmakers": ["abjad-ext-rmakers>=3.17"],
    "dev": [
        "black>=23.3.0",
        "flake8>=6.0.0",
        "isort>=5.12.0",
        "mypy>=1.2.0",
        "pytest>=7.3.1",
        "pytest-cov>=4.0.0",
        "pytest-helpers-namespace>=2021.12.29",
        "sphinx-autodoc-typehints>=1.23.0",
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
    check_python_version(version)
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
