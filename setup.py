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


with open("README.rst", "r") as file_pointer:
    long_description = file_pointer.read()


if __name__ == "__main__":
    version = get_abjad_version()
    setuptools.setup(
        author="Trevor Bača, Joséphine Wolf Oberholtzer",
        author_email="trevor.baca@gmail.com, josephine.wolf.oberholtzer@gmail.com",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Topic :: Artistic Software",
        ],
        description="Abjad is a Python API for building LilyPond files.",
        extras_require={
            "nauert": ["abjad-ext-nauert>=3.20"],
            "rmakers": ["abjad-ext-rmakers>=3.20"],
            "dev": [
                "black>=25.1.0",
                "flake8>=7.1.1",
                "isort>=6.0.0",
                "mypy>=1.14.1",
                "pytest>=8.3.4",
                "pytest-cov>=6.0.0",
                "pytest-helpers-namespace>=2021.12.29",
                "setuptools>=75.8.0",
                "sphinx>=8.1.3",
                "sphinx-rtd-theme>=3.0.2",
            ],
        },
        include_package_data=True,
        install_requires=["ply>=3.11", "roman>=5.0", "uqbar>=0.7.4"],
        keywords="lilypond, music composition, music notation",
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
