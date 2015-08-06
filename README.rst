##########
Abjad 2.16
##########

Abjad helps composers build up complex pieces of music notation in an iterative
and incremental way. Use Abjad to create symbolic representations of all the
notes, rests, staves, tuplets, beams and slurs in any score. Because Abjad
extends the `Python`_ programming language, you can use Abjad to make
systematic changes to your music as you work. And because Abjad wraps the
powerful `LilyPond`_ music notation package, you can use Abjad to control the
typographic details of the symbols on the page.

..  _LilyPond: http://lilypond.org/
..  _Python: https://www.python.org/

`GitHub`_ |
`PyPI`_ |
`Documentation <http://projectabjad.org/>`_ |
`Mailing list <http://groups.google.com/group/abjad-user>`_ |
`Issue Tracker <https://github.com/Abjad/abjad/issues>`_ |
`Travis-CI <https://travis-ci.org/Abjad/abjad>`_

..  _GitHub: https://github.com/Abjad/abjad
..  _PyPI: https://pypi.python.org/pypi/Abjad

..  image:: https://travis-ci.org/Abjad/abjad.svg?branch=master
    :target: https://travis-ci.org/Abjad/abjad

..  image:: https://img.shields.io/coveralls/Abjad/abjad.svg
    :target: https://coveralls.io/r/Abjad/abjad

Installation
============

Abjad works on Unix/Linux, OSX, and Windows.

Abjad also works with `CPython`_ versions 2.7 and 3.3+, as well as `PyPy`_.

Install Abjad
-------------

To install Abjad from `PyPI`_, the Python Package Index, via `pip`_::

    ~$ sudo pip install abjad

To install the cutting-edge version Abjad from its `GitHub`_ repository, via
`git <https://git-scm.com/>`_ and `pip`_::

    ~$ git clone https://github.com/Abjad/abjad.git 
    ~$ cd abjad
    abjad$ sudo pip install .

Install LilyPond
````````````````

Abjad uses `LilyPond`_, an open-source automated engraving engine, to produce
notational output.

Abjad targets whichever is the most recent version of `LilyPond`_. At the time
of this writing, that means 2.18-stable or 2.19-development. We recommend
installing directly from `LilyPond`_'s website, rather than using whichever
version of `LilyPond`_ your package manager provides, as these packages are
often out-of-date.

Once you have installed LilyPond, test if LilyPond is callable from your
command-line by running the following command:

..  code-block:: bash

    ~$ lilypond --version
    GNU LilyPond 2.19.20

    Copyright (c) 1996--2015 by
      Han-Wen Nienhuys <hanwen@xs4all.nl>
      Jan Nieuwenhuizen <janneke@gnu.org>
      and others.

    This program is free software.  It is covered by the GNU General Public
    License and you are welcome to change it and/or distribute copies of it
    under certain conditions.  Invoke as `lilypond --warranty` for more
    information.

If LilyPond is not callable from your command-line, you should add the
location of the LilyPond executable to your ``PATH`` environment variable.
The `LilyPond`_ documentation provides instructions for making the
``lilypond`` command available on the command-line under OSX at
http://www.lilypond.org/macos-x.html.

If you are new to working with the command-line you should use Google to
get a basic introduction to navigating in the shell, editing your profile and
setting environment variables. There are more tutorials than we can count!

Install Graphviz (optional)
```````````````````````````

Abjad uses `Graphviz`_, an open-source graph visualization library, to create
graphs of rhythm-trees and other tree structures, and to create visualizations
of class hierarchies for its documentation. Graphviz is not necessary for
creating notation with Abjad.

To install `Graphviz`_ on Debian and Ubuntu::

    ~$ sudo apt-get install graphviz

To install `Graphviz`_ on OSX via `Homebrew`_ or `MacPorts`_::

    ~$ brew install graphviz
    ~$ sudo port install graphviz

Once you have install `Graphviz`_, test if `Graphviz`_ is callable from your
command-line by running the following command:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.38.0 (20140413.2041)

Development installation
------------------------

To perform development on Abjad, run the test suite, or build Abjad's
documentation locally, clone Abjad from the Github repository and install it in
**edit mode** with its **development extras**::

    ~$ git clone https://github.com/Abjad/abjad.git
    ~$ cd abjad
    abjad$ sudo pip install -e ".[development]"

Installing Abjad in development mode will install the following `Python`_
package dependencies.

-   `pytest`_, for running Abjad's test suite

-   `Sphinx`_, for building Abjad's documentation

-   `sphinx_rtd_theme <https://pypi.python.org/pypi/sphinx_rtd_theme>`_, for
    theming Abjad's HTML documentation

-   `PyPDF2`_, for performing preprocessing on `LaTeX`_ source with Abjad's
    ``ajv book`` tool

Some of `Sphinx`_'s dependencies provide optional optimized `Python`_
extensions, which must be compiled before they can be used. If your machine
does not have a C compiler available, you may see error message while the ``pip
install -e ".[development]"`` command runs. These warnings are harmless and will
not prevent the dependencies from being installed.

To install C compilation tools on Debian and Ubuntu::

    ~$ sudo apt-get install build-essential

To install C compilation tools on OSX, we recommend simply installing XCode
from the Apple App Store. Alternatively, you can install via `Homebrew`_ or
`MacPorts`_, although this may take a significant amount of time.

Additionally, a few non-`Python`_ tools need to be installed in order to
develop Abjad or build its documentation: `TeXLive`_, `ImageMagick`_, and
`Graphviz`_ (which was explained above).

Install TeXLive
````````````````

Building the `LaTeX`_ documentation, running the test suite, and using Abjad's
``ajv book`` document preprocessing tools require `TeXLive`_.
Abjad makes use of both ``pdftex`` for producing PDFs, and the ``pdfcrop`` tool
distributed with `TeXLive`_.

To install `TeXLive`_ on Debian and Ubuntu::

    ~$ sudo apt-get install texlive-full

On OSX, we recommend installing via the `MacTeX`_ distribution.

Install ImageMagick
```````````````````

Building Abjad's documentation requires `ImageMagick`_, a collection of raster
image processing tools.

To install `ImageMagick`_ on Debian and Ubuntu:: 

    ~$ sudo apt-get install imagemagick

To install `ImageMagick`_ on OSX, we recommend installing via `Homebrew`_ or
`MacPorts`_::

    ~$ brew install imagemagick
    ~$ sudo port install imagemagick

Abjad and IPython
-----------------

Abjad can be used with `IPython`_ to embed notation, graphs and audio into an
`IPython notebook`_. To work with Abjad in `IPython`_, install Abjad with both
its **development** and **ipython** extra dependencies::

    ~$ sudo pip install abjad [development, ipython]

Capturing MIDI files into an `IPython notebook`_ requires the `fluidsynth`_
package.

To install `fluidsynth`_ on Debian or Ubuntu::

    ~$ apt-get install fluidsynth

To install `fluidsynth`_ on OSX via `Homebrew`_ or `MacPorts`_::

    ~$ brew install fluidsynth --with-libsndfile
    ~$ sudo port install fluidsynth

Once all dependencies have been installed, create a new `IPython notebook`_ and
run the following magic command in a cell to load Abjad's `IPython`_
extension::

    %load_ext abjad.ext.ipython

Virtual environments
--------------------

We strongly recommend installing Abjad into a virtual environment, especially
if you intend to hack on Abjad's own source code. Virtual environments allow
you to isolate `Python`_ packages from your systems global collection of
packages. They also allow you to install Python packages without ``sudo``. The
`virtualenv`_ package provides tools for creating Python virtual environments,
and the `virtualenvwrapper`_ package provides additional tools which make
working with virtual environments incredibly easy::

    ~$ pip install virtualenv virtualenvwrapper
    ...
    ~$ export WORKON_HOME=~/Envs
    ~$ mkdir -p $WORKON_HOME
    ~$ source /usr/local/bin/virtualenvwrapper.sh
    ~$ mkvirtualenv abjad
    ...
    ~(abjad)$ pip install abjad

If you have `virtualenvwrapper`_ installed, create a virtual environment and
install Abjad into that instead::

    ~$ mkvirtualenv abjad
    ...
    ~(abjad)$ git clone https://github.com/Abjad/abjad.git
    ~(abjad)$ cd abjad
    abjad(abjad)$ pip install -e ".[development]"

Configuring Abjad
-----------------

Abjad creates a ``~/.abjad`` directory the first time it runs. In the
``~/.abjad`` directory you will find an ``abjad.cfg`` file. This is the Abjad
configuration file. You can use the Abjad configuration file to tell Abjad
about your preferred PDF file viewer, MIDI player, LilyPond language and so on.

Your configuration file will look something like this the first time you open
it::

    # Abjad configuration file created by Abjad on 31 January 2014 00:08:17.
    # File is interpreted by ConfigObj and should follow ini syntax.

    # Set to the directory where all Abjad-generated files
    # (such as PDFs and LilyPond files) should be saved.
    # Defaults to $HOME.abjad/output/
    abjad_output_directory = /Users/username/.abjad/output

    # Default accidental spelling (mixed|sharps|flats).
    accidental_spelling = mixed

    # Comma-separated list of LilyPond files that 
    # Abjad will "\include" in all generated *.ly files
    lilypond_includes = ,

    # Language to use in all generated LilyPond files.
    lilypond_language = english

    # Lilypond executable path. Set to override dynamic lookup.
    lilypond_path = lilypond

    # MIDI player to open MIDI files.
    # When unset your OS should know how to open MIDI files.
    midi_player = 

    # PDF viewer to open PDF files.
    # When unset your OS should know how to open PDFs.
    pdf_viewer = 

    # Text editor to edit text files.
    # When unset your OS should know how to open text files.
    text_editor = 

Follow the basics of ``ini`` syntax when editing the Abjad configuration file.
Background information is available at http://en.wikipedia.org/wiki/INI_file.
Under MacOS you might want to set you ``midi_player`` to iTunes. Under Linux
you might want to set your ``pdf_viewer`` to ``evince`` and your
``midi_player`` to ``tiMIDIty``, and so on.

..  _CPython: http://www.python.org
..  _GitHub: https://github.com/Abjad/abjad
..  _Graphviz: http://graphviz.org/
..  _Homebrew: http://brew.sh/
..  _IPython notebook: http://ipython.org/notebook.html
..  _IPython: http://ipython.org/
..  _ImageMagick: http://www.imagemagick.org/script/index.php
..  _LaTeX: https://tug.org/
..  _LilyPond: http://lilypond.org/
..  _MacPorts: https://www.macports.org/
..  _MacTeX: https://tug.org/mactex/
..  _PyPDF2: http://pythonhosted.org/PyPDF2/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _PyPy: http://pypy.org/
..  _Python: https://www.python.org/
..  _Sphinx: http://sphinx-doc.org/
..  _TeXLive: https://www.tug.org/texlive/
..  _fluidsynth: http://www.fluidsynth.org/
..  _pip: https://pip.pypa.io/en/stable/
..  _pytest: http://pytest.org/latest/
..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/