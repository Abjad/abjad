#####
Abjad
#####

Abjad helps composers build up complex pieces of music notation in an iterative and incremental way. Use Abjad to create symbolic representations of all the notes, rests, staves, tuplets, beams and slurs in any score. Because Abjad extends the `Python`_ programming language, you can use Abjad to make systematic changes to your music as you work. And because Abjad wraps the powerful `LilyPond`_ music notation package, you can use Abjad to control the typographic details of the symbols on the page.

..  _LilyPond: http://lilypond.org/
..  _Python: https://www.python.org/

`GitHub`_ |
`PyPI`_ |
`Documentation <https://abjad.github.io/>`_ |
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

..  image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

Abjad works on Unix / Linux, OSX and Windows. Abjad requires Python 3.6 or later.

Installation
============

If you're new to Abjad and you want to get started right away, follow the easy install instructions. If you're a more experienced Abjad user and you want to build Abjad's documentation, run Abjad's tests or add features to Abjad, then follow the developer install instructions. Whichever install you chose, you'll first need to install LilyPond and make sure that LilyPond is callable on your commandline.

Install LilyPond
----------------

`LilyPond`_ is an open-source program that engraves music notation in an automated way. Abjad uses LilyPond to produce notational output. Because package managers sometimes provide out-of-date versions of LilyPond we recommend installing the most recent version of LilyPond directly from the LilyPond website. After you install LilyPond, check to see if LilyPond is callable from your commandline::

    ~$ lilypond --version

    GNU LilyPond 2.19.83

    Copyright (c) 1996--2015 by
      Han-Wen Nienhuys <hanwen@xs4all.nl>
      Jan Nieuwenhuizen <janneke@gnu.org>
      and others.

    This program is free software.  It is covered by the GNU General Public
    License and you are welcome to change it and/or distribute copies of it
    under certain conditions.  Invoke as `lilypond --warranty` for more
    information.

If LilyPond is not callable from your commandline, you can follow the instructions provided at http://www.lilypond.org/macos-x.html. Alternatively, add the location of the LilyPond executable to your ``PATH`` environment variable. Under OSX you can update your path like this:

..  code-block:: bash

    export PATH="$PATH:/Applications/LilyPond.app/Contents/Resources/bin/"

**NOTE: OSX users should be aware that the LilyPond development team is currently experiencing difficulties publishing LilyPond for Apple's 10.15 (Catalina) series of releases.** This problem seems nearly certain to be resolved at some point. But, in the meantime, OSX users who have upgraded to 10.15 must inquire on the LilyPond user list to find an interim-compiled version of LilyPond that is not yet available on LilyPond downloads page. **OSX users still using Apple's 10.14 (Mojave) series of releases will experience no problems and should download the most recent version of LilyPond from the LilyPond downloads page.**

Easy install or developer install?
----------------------------------

After  you've installed LilyPond you can decide whether to follow Abjad easy install instructions or Abjad developer install instructions. Whichever install you chose, consider setting up Python virtual environments on your computer before you begin. Python virtual environments ease the work involved in managing the ways that different versions of Python interact with the Python packages you install on your computer. Abjad development install instructions assume you will be working in a Python virtual environment. Users following an easy install are recommended to consider installing Abjad in a Python virtual environment, too. `Click here for instructions on setting up Python virtual environments on your computer. <https://abjad.github.io/virtualenv.html>`_

A. Easy install
===============

Install Abjad like this:

..  code-block:: bash

    ~$ pip install abjad

After installation, check that Python can import Abjad:

..  code-block:: bash

    ~$ python
    Python 3.7.4 (v3.7.4:e09359112e, Jul  8 2019, 14:54:52) 
    [Clang 6.0 (clang-600.0.57)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import abjad
    >>> abjad.__version__
    '3.1'

Congratulations! Easy install is complete after you install LilyPond and Abjad. Skip section B of this document. Look over optional sections C, D and E. Then read through the tutorials and examples for ideas about where to go next.

B. Developer install
====================

Abjad has been actively developed for more than ten years. Follow these instructions if you want to follow the cutting-edge of Abjad development, build Abjad's documentation, run Abjad's tests or add new features to Abjad.

Before you begin:

* Make sure LilyPond is installed and callable from the commandline
* Create a Python virtual environment to install Abjad

B.1 Clone the Abjad repository
------------------------------

Make sure you've created a Python virtual environment for Abjad. Make sure the virtual environment is active. Then clone Abjad from the Github repository:

..  code-block:: bash

    ~(abjad)$ git clone https://github.com/Abjad/abjad.git

B.2 Install Abjad
-----------------

Make sure you've created a Python virtual environment for Abjad. Make sure the virtual environment is active. Then change into your Abjad clone and install Abjad in **edit mode** with **development extras**:

..  code-block:: bash

    ~(abjad)$ cd abjad
    abjad(abjad)$ sudo pip install -e .[development]  # NOTE: no spaces in the string after "install"

Development mode will install `pytest`_ and `Sphinx`_ on your system. Abjad uses pytest to test the Abjad codeabase. Abjad uses Sphinx to build the Abjad documentation. Some of Sphinx's dependencies provide optional Python extensions that must be compiled before they can be used. If your machine does not have a C compiler available, you may see error message while ``pip install -e ".[development]"`` runs. These warnings are harmless and will not stop installation. 

B.3 Install Graphviz (optional)
-------------------------------

`Graphviz`_ is an open-source graph visualization library. Abjad uses Graphviz to to graph treelike structures, like rhythm-trees and the inheritance relations of Abjad classes. You don't need Graphviz to create notation with Abjad. But you can install Graphviz if you want to build the most recent version of Abjad's documentation on your computer:

Install Graphviz on Debian and Ubuntu like this:

..  code-block:: bash

    ~$ sudo apt-get install graphviz

Install Graphviz on OSX via Homebrew like this:

..  code-block:: bash

    ~$ brew install graphviz

Test if Graphviz is callable from your commandline like this:

..  code-block:: bash

    ~$ dot -V
    dot - graphviz version 2.40.1 (20161225.0304)

B.4 Start developing
--------------------

Congratulations! Developer install is complete after you install LilyPond, set up a virtual environment, and clone and install Abjad. (You may optionally have installed Graphviz to build Abjad's documentation, too.) Look through sections C, D and E of this document. Then read through Abjad's tutorials and examples for ideas about where to go next.

C. Using Abjad with IPython notebooks (optional)
================================================

Abjad can be used with `IPython`_ to embed music notation, graphs and audio into an `IPython notebook`_.

To work with Abjad in IPython, install Abjad with both its **development** and **ipython** extra dependencies:

..  code-block:: bash

    ~$ sudo pip install abjad[ipython]  # NOTE: no spaces in the string after "install"

Capturing MIDI files into an IPython notebook requires the `timidity`_ package. To install timidity on Debian or Ubuntu:

..  code-block:: bash

    ~$ apt-get install timidity

To install timidity on OSX via Homebrew:

..  code-block:: bash

    ~$ brew install timidity

Create a new IPython notebook and run the following magic command in a cell to load Abjad's IPython extension. Once loaded, notation and MIDI files can be embedded in your notebook whenever you use ``abjad.show()`` and ``abjad.play()`` on valid Abjad objects::

    %load_ext abjadext.ipython

D. Installing Abjad extension packages (optional)
=================================================

After you work with Abjad for a while you may be interested in Abjad's extension packages.

Pick the extensions you want and then install them like this:

..  code-block:: bash

    ~$ pip install abjad[cli]       # score package commandline tools 
    ~$ pip install abjad[ipython]   # ipython integration 
    ~$ pip install abjad[nauert]    # quantization tools
    ~$ pip install abjad[rmakers]   # rhythm-maker tools
    ~$ pip install abjad[tonality]  # tonal analysis tools

E. Configuring Abjad
====================

Abjad creates a ``~/.abjad`` directory the first time it runs. In the ``~/.abjad`` directory you will find an ``abjad.cfg`` file. This is the Abjad configuration file. You can use the Abjad configuration file to tell Abjad about your preferred PDF file viewer, MIDI player, LilyPond language and so on. Your configuration file will look something like this the first time you open it:

::

    # Abjad configuration file created by Abjad on 31 January 2014 00:08:17.
    # File is interpreted by ConfigObj and should follow ini syntax.

    # Set to the directory where all Abjad-generated files
    # (such as PDFs and LilyPond files) should be saved.
    # Defaults to $HOME.abjad/output/
    abjad_output_directory = /Users/username/.abjad/output

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

Follow ``ini`` syntax when editing the Abjad configuration file. Background information is available at http://en.wikipedia.org/wiki/INI_file. Under MacOS you might want to set you ``midi_player`` to iTunes. Under Linux you might want to set your ``pdf_viewer`` to ``evince`` and your ``midi_player`` to ``tiMIDIty``.

..  _CPython: http://www.python.org
..  _GitHub: https://github.com/Abjad/abjad
..  _Graphviz: http://graphviz.org/
..  _Homebrew: http://brew.sh/
..  _IPython notebook: http://ipython.org/notebook.html
..  _IPython: http://ipython.org/
..  _LilyPond: http://lilypond.org/
..  _PyPI: https://pypi.python.org/pypi/Abjad
..  _Python: https://www.python.org/
..  _Sphinx: http://sphinx-doc.org/
..  _timidity: http://timidity.sourceforge.net/
..  _pip: https://pip.pypa.io/en/stable/
..  _pytest: http://pytest.org/en/latest/
..  _virtualenv: https://readthedocs.org/projects/virtualenv/
..  _virtualenvwrapper: https://virtualenvwrapper.readthedocs.org/en/latest/
