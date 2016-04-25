##########
Abjad 2.18
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

..  image:: https://img.shields.io/travis/Abjad/abjad/master.svg?style=flat-square
    :target: https://travis-ci.org/Abjad/abjad

..  image:: https://img.shields.io/coveralls/Abjad/abjad/master.svg?style=flat-square
    :target: https://coveralls.io/r/Abjad/abjad

..  image:: https://img.shields.io/pypi/v/abjad.svg?style=flat-square
    :target: https://pypi.python.org/pypi/abjad

..  image:: https://img.shields.io/pypi/dm/abjad.svg?style=flat-square
    :target: https://pypi.python.org/pypi/abjad

Installation
============

Abjad works on Unix/Linux, OSX, and Windows.

Abjad also works with `CPython`_ versions 2.7 and 3.3+, as well as `PyPy`_.

Install Abjad
-------------

To install the most recent official release of Abjad from `PyPI`_, the Python
Package Index, via `pip`_:

..  code-block:: bash

    ~$ sudo pip install abjad

**Caution**:

    We strongly encourage you to *not* install Abjad globally via ``sudo pip
    install``, but to use a virtual environment instead. If you're already
    working in a virtual environment, simply omit the ``sudo``.

**Note**:

    Abjad supports Python 2.7 and above. Python 2.7.9 and above provide `pip`_
    out-of-the-box. For earlier versions of Python 2.7, you may need to install
    `pip`_ yourself. While you can use the old ``easy_install`` tool (``sudo
    easy_install pip``), we strongly recommend the `pip`_-installation
    instructions found here: https://pip.pypa.io/en/stable/installing/.

To install the cutting-edge version Abjad from its `GitHub`_ repository, via
`git <https://git-scm.com/>`_ and `pip`_:

..  code-block:: bash

    ~$ git clone https://github.com/Abjad/abjad.git 
    ~$ cd abjad
    abjad$ sudo pip install .

Once you have Abjad installed, fire up Python and import it:

..  code-block:: bash

    $ python
    Python 2.7.9 (default, Nov  9 2015, 10:50:36) 
    [GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.1.76)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import abjad
    >>> abjad.__version__
    '2.16'

Congratulations!

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

If LilyPond is not callable from your command-line, you should add the location
of the LilyPond executable to your ``PATH`` environment variable. If you are
using OSX, simply run the following line in your terminal:

..  code-block:: bash

    export PATH="$PATH:/Applications/LilyPond.app/Contents/Resources/bin/"

You can add the above line to your ``~/.profile`` to make the change permanent.

The `LilyPond`_ documentation also provides instructions for making the
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

To install `Graphviz`_ on Debian and Ubuntu:

..  code-block:: bash

    ~$ sudo apt-get install graphviz

To install `Graphviz`_ on OSX via `Homebrew`_:

..  code-block:: bash

    ~$ brew install graphviz

Once you have install `Graphviz`_, test if `Graphviz`_ is callable from your
command-line by running the following command:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.38.0 (20140413.2041)

All of the graph images in Abjad's API documentation were created via
`graphviz`_. See the API entry for `topleveltools.graph()` for more details.

Development installation
------------------------

To perform development on Abjad, run the test suite, or build Abjad's
documentation locally, clone Abjad from the Github repository and install it in
**edit mode** with its **development extras**:

..  code-block:: bash

    ~$ git clone https://github.com/Abjad/abjad.git
    ~$ cd abjad
    abjad$ sudo pip install -e .[development]  # NOTE: no spaces in the string after "install"

Installing Abjad in development mode will install the following `Python`_
package dependencies (along with their own dependencies):

-   `pytest`_, for running Abjad's test suite

-   `Sphinx`_, for building Abjad's documentation

-   `PyPDF2`_, for performing preprocessing on `LaTeX`_ source with Abjad's
    ``ajv book`` tool

Some of `Sphinx`_'s dependencies provide optional optimized `Python`_
extensions, which must be compiled before they can be used. If your machine
does not have a C compiler available, you may see error message while the ``pip
install -e ".[development]"`` command runs. These warnings are harmless and will
not prevent the dependencies from being installed.

To install C compilation tools on Debian and Ubuntu:

..  code-block:: bash

    ~$ sudo apt-get install build-essential

To install C compilation tools on OSX, we recommend simply installing XCode
from the Apple App Store. Alternatively, you can install via `Homebrew`_
although this may take a significant amount of time.

Additionally, a few non-`Python`_ tools need to be installed in order to
develop Abjad or build its documentation: `TeXLive`_, `ImageMagick`_, and
`Graphviz`_ (which was explained above).

Install TeXLive
````````````````

Building the `LaTeX`_ documentation, running the test suite, and using Abjad's
``ajv book`` document preprocessing tools require `TeXLive`_.
Abjad makes use of both ``pdftex`` for producing PDFs, and the ``pdfcrop`` tool
distributed with `TeXLive`_.

To install `TeXLive`_ on Debian and Ubuntu:

..  code-block:: bash

    ~$ sudo apt-get install texlive-full

On OSX, we recommend installing via the `MacTeX`_ distribution.

Install ImageMagick
```````````````````

Building Abjad's documentation requires `ImageMagick`_, a collection of raster
image processing tools.

To install `ImageMagick`_ on Debian and Ubuntu:

..  code-block:: bash

    ~$ sudo apt-get install imagemagick

To install `ImageMagick`_ on OSX, we recommend installing via `Homebrew`_:

..  code-block:: bash

    ~$ brew install imagemagick

Once you have install `ImageMagick`_, test if `ImageMagick`_ is callable from
your command-line by running the following command:

..  code-block:: bash

    ~$ convert --version
    Version: ImageMagick 6.9.1-6 Q16 x86_64 2015-06-22 http://www.imagemagick.org
    Copyright: Copyright (C) 1999-2015 ImageMagick Studio LLC
    License: http://www.imagemagick.org/script/license.php
    Features: Cipher DPC Modules 
    Delegates (built-in): bzlib freetype jng jpeg ltdl lzma png tiff xml zlib

Abjad and IPython
-----------------

Abjad can be used with `IPython`_ to embed notation, graphs and audio into an
`IPython notebook`_. To work with Abjad in `IPython`_, install Abjad with both
its **development** and **ipython** extra dependencies:

..  code-block:: bash

    ~$ sudo pip install abjad[development,ipython]  # NOTE: no spaces in the string after "install"

Capturing MIDI files into an `IPython notebook`_ requires the `timidity`_
package.

To install `timidity`_ on Debian or Ubuntu:

..  code-block:: bash

    ~$ apt-get install timidity

To install `timidity`_ on OSX via `Homebrew`_:

..  code-block:: bash

    ~$ brew install timidity

Once all dependencies have been installed, create a new `IPython notebook`_ and
run the following "magic" command in a cell to load Abjad's `IPython`_
extension::

    %load_ext abjad.ext.ipython

Once loaded, notation and MIDI files can be embedded in your notebook whenever
you use `show(...)` and `play(...)` on valid Abjad objects.

..  _virtual-environments:

Virtual environments
--------------------

We strongly recommend installing Abjad into a virtual environment, especially
if you intend to hack on Abjad's own source code. Virtual environments allow
you to isolate `Python`_ packages from your systems global collection of
packages. They also allow you to install Python packages without ``sudo``. The
`virtualenv`_ package provides tools for creating Python virtual environments,
and the `virtualenvwrapper`_ package provides additional tools which make
working with virtual environments incredibly easy.

Let's install `virtualenvwrapper`_:

..  code-block:: bash

    ~$ sudo pip install virtualenvwrapper
    ...

**Note**:

    On OSX 10.11 (El Capitan) it may be necessary to install
    `virtualenvwrapper`_ via alternate instructions:

    ..  code-block:: bash

        ~$ pip install virtualenvwrapper --ignore-installed six

    See
    `here <http://stackoverflow.com/questions/32086631/cant-install-virtualenvwrapper-on-osx-10-11-el-capitan>`_
    for details.

Next, set an environment variable in your shell naming the directory you want
the virtual environment files to be stored in, then create that directory if it
doesn't already exist:

..  code-block:: bash

    ~$ export WORKON_HOME=~/.virtualenvs
    ~$ mkdir -p $WORKON_HOME

**Note**:

    The location your virtual environment files are stored in could be
    anywhere. Because you are unlikely to need to access them directly, we
    suggest the `.`-prepended path ``.virtualenvs``.

With the virtual environment directory created, "source" `virtualenvwrapper`_'s
script. This script teaches your shell about how to create, activate and delete
virtual environments:

..  code-block:: bash

    ~$ source `which virtualenvwrapper.sh`

Finally, you can create a virtual environment via the ``mkvirtualenv`` command.
This will both create the fresh environment and "activate" it. Once activated,
you can install Python packages within that environment, safe in the knowledge
that they won't interfere with Python packages installed anywhere else on your
system:

..  code-block:: bash

    ~$ mkvirtualenv abjad
    ...
    ~(abjad)$ pip install abjad  # "(abjad)" indicates the name of the virtualenv
    ...

You can also deactivate the current virtual environment via the ``deactivate``
command, or switch to a different environment via the ``workon <virtualenv
name>`` command:

..  code-block:: bash

    ~(abjad)$ deactivate
    ~$ workon my-new-score
    ~(my-new-score)$

To make the virtual environment configuration sticky from terminal session to
terminal session, add the following lines to your ``~/.profile``,
``~/.bash_profile`` or similar shell configuration file:

..  code-block:: bash

    export WORKON_HOME=$HOME/.virtualenvs
    source `which virtualenvwrapper.sh`

Development installation within a virtualenv
````````````````````````````````````````````

To recap, a complete development installation of Abjad within a virtual
environment requires the following steps:

- Create and activate a new virtual environment
- Clone Abjad somewhere and ``cd`` into the root of the cloned repository
- Install Abjad and its development / IPython dependencies

..  code-block:: bash

    ~$ mkvirtualenv abjad
    ...
    ~(abjad)$ git clone https://github.com/Abjad/abjad.git
    ~(abjad)$ cd abjad
    abjad(abjad)$ pip install -e .[development,ipython]  # NOTE: no spaces between "." and "[development,ipython]"
    ...

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
..  _MacTeX: https://tug.org/mactex/
..  _PyPDF2: http://pythonhosted.org/PyPDF2/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _PyPy: http://pypy.org/
..  _Python: https://www.python.org/
..  _Sphinx: http://sphinx-doc.org/
..  _TeXLive: https://www.tug.org/texlive/
..  _timidity: http://timidity.sourceforge.net/
..  _pip: https://pip.pypa.io/en/stable/
..  _pytest: http://pytest.org/latest/
..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
