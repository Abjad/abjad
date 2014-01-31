abjad
=====

Abjad helps composers build up complex pieces of music notation in an iterative
and incremental way.

Use Abjad to create a symbolic representation of all the notes, rests, staves,
tuplets, beams and slurs in any score.

Because Abjad extends the Python programming language, you can use Abjad to
make systematic changes to your music as you work. And because Abjad wraps the
powerful LilyPond music notation package, you can use Abjad to control the
typographic details of the symbols on the page.

You can find Abjad's documentation here:
[http://projectabjad.org](http://projectabjad.org)


Installation
------------

This install file refers to the 2.x releases of Abjad.


Abjad depends on Python
-----------------------

You must have Python 2.7.5 installed to run Abjad.

Abjad also depends on the following Python packages:

    * configobj
    * ply
    * pytest
    * Sphinx

Type the following to check the version of Python installed on your computer:

    python --version

Abjad does not yet support the Python 3.x series of releases.

You can download different versions of Python at http://www.python.org.


Abjad depends on LilyPond
-------------------------

You must have LilyPond 2.17 or greater installed for Abjad to work properly.

You can download LilyPond at http://www.lilypond.org.

After you have installed LilyPond you should type the following to see if
LilyPond is callable from your commandline:

    lilypond --version

If LilyPond is not callable from your commandline you
should add the location of the LilyPond executable to your ``PATH``
environment variable.


Documentation
-------------

Online documentation for the most recent release of Abjad is available at
http://projectabjad.org.

You will find a PDF version of the documentation in Abjad's ``abjad/docs/pdf/``
directory after you install the package.

Most users will find the online or PDF version of the docs sufficient. If you
work with Abjad lot and decide to add code to Abjad that you want to contribute
back to the project, it will probably make sense to build a local copy of the
docs for yourself as you work. To build Abjad's docs locally you'll need to
install Graphviz. See http://graphviz.org/ for instructions.


Installing the current packaged version of Abjad with pip
---------------------------------------------------------

There are different ways to install Python packages on your computer. One of
the most direct ways is with ``pip``. This is the package management tool
recommended by the Python Package Index (https://pypi.python.org/pypi).

Type the following to find out if ``pip`` is installed on your computer:

    pip --version

If you do not have ``pip`` installed then we strongly recommend that you use
Python's ``easy_install`` to install ``pip``.

    sudo easy_install pip

Once ``pip`` is available on your computer you'll be ready to install Abjad.

Type the following to install the current packaged version of Abjad:

    sudo pip install abjad --upgrade

Python will install Abjad in the site packages directory on your computer and
you'll be ready to start using the system.


Manually installing Abjad from the Python Package Index
-------------------------------------------------------

If you do not have ``pip`` or ``easy_install`` installed on your computer you
then should follow these steps to install the current packaged version of Abjad
from the Python Package Index:

1.  Download the current release of Abjad from 
    http://pypi.python.org/pypi/Abjad.

2.  Unarchive the downloaded file. Under MacOS and Windows you can 
    double click the archived file.

    Under Linux execute the following command with ``x.y`` replaced by 
    the current release of Abjad:
    
        tar xzvf Abjad-x.y.tar.gz
    
3.  Change into the directory created in step 2:

        cd Abjad-x.y

4.  Run the following under MacOS or Linux:

        sudo python setup.py install

5.  Or run this command under Windows after starting up a command shell 
    with administrator privileges:

        setup.py install

These commands will cause Python to install Abjad in your site packages
directory. You'll then be ready to start using Abjad.


Configuring Abjad
-----------------

Abjad creates a ``~/.abjad`` directory the first time it runs.  In ``~/.abjad``
you will find a the file ``abjad.cfg``.  This is the Abjad configuration file.
You can use the Abjad configuration file to tell Abjad about your preferred PDF
file viewer, MIDI player, your preferred LilyPond language and so on.

Your configuration file's contents will look approximately like
this by default:

    # Abjad configuration file created by Abjad on 31 January 2014 00:08:17.
    # File is interpreted by ConfigObj and should follow ini syntax.

    # Set to the directory where all Abjad-generated files
    # (such as PDFs and LilyPond files) should be saved.
    # Defaults to $HOME.abjad/output/
    abjad_output = /Users/josiah/.abjad/output

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

In Linux, for example, you might want to set your ``pdf_viewer`` to ``evince``
and your ``midi_player`` to ``tiMIDIty``.

The configuration file is in ``ini`` syntax. So make sure to follow ``ini``
syntax conventions when editing your Abjad configuration file.
