#! /usr/bin/env python
import os
import setuptools


version_file_path = os.path.join(
    os.path.dirname(__file__),
    'abjad',
    '_version.py'
    )
with open(version_file_path, 'r') as file_pointer:
    file_contents_string = file_pointer.read()
local_dict = {}
exec(file_contents_string, None, local_dict)
__version__ = local_dict['__version__']

description = 'Abjad is a Python API for Formalized Score Control.'

with open('README.rst', 'r') as file_pointer:
    long_description = file_pointer.read()

author = [
    'Trevor Bača',
    'Josiah Wolf Oberholtzer',
    'Víctor Adán',
    ]
author = ', '.join(author)

author_email = [
    'trevor.baca@gmail.com',
    'josiah.oberholtzer@gmail.com',
    'contact@victoradan.net',
    ]
author_email = ', '.join(author_email)

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Artistic Software',
    ]

entry_points = {
    'console_scripts': [
        'ajv = abjad.cli:run_ajv',
        ]
    }

extras_require = {
    'accelerated': ['quicktions>=1.3'],
    'book': ['abjad-ext-book >= 3.0.0, < 3.1.0'],
    'cli': ['abjad-ext-cli >= 3.0.0, < 3.1.0'],
    'ipython': ['abjad-ext-ipython >= 3.0.0, < 3.1.0'],
    'nauert': ['abjad-ext-nauert >= 3.0.0, < 3.1.0'],
    'rmakers': ['abjad-ext-rmakers >= 3.0.0, < 3.1.0'],
    'tonality': ['abjad-ext-tonality >= 3.0.0, < 3.1.0'],
    'test': [
        'mypy',
        'pytest>=3.5.0',
        'pytest-cov',
        'pytest-helpers-namespace',
        ],
    }

keywords = [
    'music composition',
    'music notation',
    'formalized score control',
    'lilypond',
    ]
keywords = ', '.join(keywords)

install_requires = [
    'ply',
    'roman',
    'uqbar>=0.2.15',
    ]

if __name__ == '__main__':
    setuptools.setup(
        author=author,
        author_email=author_email,
        classifiers=classifiers,
        description=description,
        entry_points=entry_points,
        extras_require=extras_require,
        include_package_data=True,
        install_requires=install_requires,
        keywords=keywords,
        license='MIT',
        long_description=long_description,
        name='Abjad',
        packages=['abjad'],
        platforms='Any',
        url='http://www.projectabjad.org',
        version=__version__,
        )
