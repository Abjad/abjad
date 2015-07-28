# Abjad

Abjad helps composers build up complex pieces of music notation in an iterative and incremental way. Use Abjad to create a symbolic representation of all the notes, rests, staves, tuplets, beams and slurs in any score. Because Abjad extends the Python programming language, you can use Abjad to make systematic changes to your music as you work. And because Abjad wraps the powerful LilyPond music notation package, you can use Abjad to control the typographic details of the symbols on the page.

Abjad's documentation is available at http://projectabjad.org.

[![Build Status](https://travis-ci.org/Abjad/abjad.svg?branch=master)](https://travis-ci.org/Abjad/abjad)
[![Coverage Status](https://img.shields.io/coveralls/Abjad/abjad.svg)](https://coveralls.io/r/Abjad/abjad)
[![Downloads](https://pypip.in/download/Abjad/badge.svg)](https://pypi.python.org/pypi/Abjad/)
[![Latest Version](https://pypip.in/version/Abjad/badge.svg)](https://pypi.python.org/pypi/Abjad/)

## Installing Abjad

### Python and OS Support

Abjad works with [CPython] versions 2.7 and 3.3+.

Abjad works on Unix/Linux, OSX, and Windows.

To check the version of [Python] installed on your computer, type the
following:

    ~$ python --version
    Python 2.7.10

### Install Abjad

To install Abjad from [PyPI], the Python Package Index, via [pip]:

    ~$ sudo pip install abjad

To install the cutting-edge version Abjad from its [GitHub] repository, via
[git](https://git-scm.com/) and [pip]:

    ~$ git clone https://github.com/Abjad/abjad.git 
    ~$ cd abjad
    abjad$ sudo pip install .

### Install LilyPond

Abjad uses [LilyPond], an open-source automated engraving engine, to produce
notational output. Abjad targets whichever is the most recent version of
[LilyPond]. We recommend installing directly from [LilyPond]'s website,
rather than using whichever version of [LilyPond] your package manager
provides, as these packages are often out-of-date.

Once you have installed LilyPond, test if LilyPond is callable from your
command-line by running the following command:

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
The [LilyPond] documentation provides instructions for making the
``lilypond`` command available on the command-line under OSX at
http://www.lilypond.org/macos-x.html.

If you are new to working with the command-line you should use Google to
get a basic introduction to editing your profile and setting environment
variables.

### Install Graphviz (optional)

Abjad uses [Graphviz], an open-source graph visualization library, to create
graphs of rhythm-trees and other tree structures, and to create visualizations
of class hierarchies for its documentation. Graphviz is not necessary for
creating notation with Abjad.

To install [Graphviz] on Debian and Ubuntu::

    ~$ sudo apt-get install graphviz

To install [Graphviz] on OSX via [Homebrew] or [MacPorts]::

    ~$ brew install graphviz
    ~$ sudo port install graphviz

Once you have install [Graphviz], test if [Graphviz] is callable from your
command-line by running the following command:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.38.0 (20140413.2041)

## Development installation

To perform development on Abjad, run the test suite, or build Abjad's
documentation locally, clone Abjad from the Github repository and install it in
**edit mode** with its **development extras**::

    ~$ git clone https://github.com/Abjad/abjad.git
    ~$ cd abjad
    abjad$ sudo pip install -e . [development]

Installing Abjad in development mode will install the following [Python]
package dependencies.

-   [pytest], for running Abjad's test suite

-   [Sphinx], for building Abjad's documentation

-   [sphinx_rtd_theme](https://pypi.python.org/pypi/sphinx_rtd_theme), for
    theming Abjad's HTML documentation

-   [sphinxcontrib-images](<https://github.com/spinus/sphinxcontrib-images/),
    for handling image thumbnails in Abjad's HTML documentation

-   [PyPDF2], for performing preprocessing on [LaTeX] source with Abjad's
    ``ajv book`` tool

Some of [Sphinx]'s dependencies provide optional optimized [Python]
extensions, which must be compiled before they can be used. If your machine
does not have a C compiler available, you may see error message while the ``pip
install -e . [development]`` command runs. These warnings are harmless and will
not prevent the dependencies from being installed.

To install C compilation tools on Debian and Ubuntu::

    ~$ sudo apt-get install build-essential

To install C compilation tools on OSX, we recommend simply installing XCode
from the Apple App Store. Alternatively, you can install via [Homebrew] or
[MacPorts], although this may take a significant amount of time.

Additionally, a few non-[Python] tools need to be installed in order to
develop Abjad or build its documentation: [TeXLive], [ImageMagick], and
[Graphviz] (which was explained above).

### TexLive

Building the [LaTeX] documentation, running the test suite, and using Abjad's
``ajv book`` document preprocessing tools require [TeXLive].
Abjad makes use of both ``pdftex`` for producing PDFs, and the ``pdfcrop`` tool
distributed with [TeXLive].

To install [TeXLive] on Debian and Ubuntu::

    ~$ sudo apt-get install texlive-full

On OSX, we recommend installing via the [MacTeX] distribution.

### ImageMagick

Building Abjad's documentation requires [ImageMagick], a collection of raster
image processing tools.

To install [ImageMagick] on Debian and Ubuntu:: 

    ~$ sudo apt-get install imagemagick

To install [ImageMagick] on OSX, we recommend installing via [Homebrew] or
[MacPorts]:

    ~$ brew install imagemagick
    ~$ sudo port install imagemagick

## Abjad and IPython

Abjad can be used with [IPython] to embed notation, graphs and audio into an
[IPython notebook]. To work with Abjad in [IPython], install Abjad with both
its **development** and **ipython** extra dependencies::

    ~$ sudo pip install abjad [development, ipython]

Capturing MIDI files into an [IPython notebook] requires the [fluidsynth]
package.

To install [fluidsynth] on Debian or Ubuntu::

    ~$ apt-get install fluidsynth

To install [fluidsynth] on OSX via [Homebrew] or [MacPorts]::

    ~$ brew install fluidsynth --with-libsndfile
    ~$ sudo port install fluidsynth

Once all dependencies have been installed, create a new [IPython notebook] and
run the following magic command in a cell to load Abjad's [IPython]
extension:

    %load_ext abjad.ext.ipython

## Virtual environments

We strongly recommend installing Abjad into a virtual environment, especially
if you intend to hack on Abjad's own source code. Virtual environments allow
you to isolate [Python] packages from your systems global collection of
packages. They also allow you to install Python packages without ``sudo``. The
[virtualenv] package provides tools for creating Python virtual environments,
and the [virtualenvwrapper] package provides additional tools which make
working with virtual environments incredibly easy::

    ~$ pip install virtualenv virtualenvwrapper
    ...
    ~$ export WORKON_HOME=~/Envs
    ~$ mkdir -p $WORKON_HOME
    ~$ source /usr/local/bin/virtualenvwrapper.sh
    ~$ mkvirtualenv abjad
    ...
    ~(abjad)$ pip install abjad

If you have [virtualenvwrapper] installed, create a virtual environment and
install Abjad into that instead:

    ~$ mkvirtualenv abjad
    ...
    ~(abjad)$ git clone https://github.com/Abjad/abjad.git
    ~(abjad)$ cd abjad
    abjad(abjad)$ pip install -e . [development]

[CPython]: http://www.python.org
[GitHub]: https://github.com/Abjad/abjad
[Graphviz]: http://graphviz.org/
[Homebrew]: http://brew.sh/
[IPython notebook]: http://ipython.org/notebook.html
[IPython]: http://ipython.org/
[ImageMagick]: http://www.imagemagick.org/script/index.php
[LaTeX]: https://tug.org/
[LilyPond]: http://lilypond.org/
[MacPorts]: https://www.macports.org/
[MacTeX]: https://tug.org/mactex/
[PyPDF2]: http://pythonhosted.org/PyPDF2/
[PyPI]: https://pypi.python.org/pypi/Abjad
[Python]: https://www.python.org/
[Sphinx]: http://sphinx-doc.org/
[TeXLive]: https://www.tug.org/texlive/
[fluidsynth]: http://www.fluidsynth.org/
[pip]: https://pip.pypa.io/en/stable/
[pytest]: http://pytest.org/latest/
[virtualenv]: https://readthedocs.org/projects/virtualenv/
[virtualenvwrapper]: https://virtualenvwrapper.readthedocs.org/en/latest/
