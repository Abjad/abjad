Installation
============


Abjad depends on Python
-----------------------

You must have Python 2.7 or 3.3+ installed to run Abjad.

To check the version of Python installed on your computer type the following:

.. code-block:: bash

    python --version

You can download different versions of Python at http://www.python.org.


Abjad depends on LilyPond
-------------------------

You must have LilyPond 2.18 or greater installed for Abjad to work properly.

You can download LilyPond at http://www.lilypond.org.

After you have installed LilyPond you should type the following to see if
LilyPond is callable from your command-line:

.. code-block:: bash

    lilypond --version

If LilyPond is not callable from your command-line you
should add the location of the LilyPond executable to your ``PATH``
environment variable.

If you are new to working with the command-line 
you should use Google to get a basic introduction to 
editing your profile and setting environment variables.


Installing the current packaged version of Abjad with ``pip``
-------------------------------------------------------------

There are different ways to install Python packages on your computer. One of
the most direct ways is with ``pip``, the package management tool recommended
by the `Python Package Index <https://pypi.python.org/pypi>`_.

..  code-block:: bash

    sudo pip install abjad --upgrade

Python will install Abjad in the site packages directory on your computer and
you'll be ready to start using the system.

If you don't have ``pip``, but you do have Python's ``easy_install`` (as is
often the case), we strongly recommend using ``easy_install`` to install
``pip``, and then ``pip`` to install Abjad.

..  code-block:: bash

    sudo easy_install pip


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
    
    .. code-block:: bash

        tar xzvf Abjad-x.y.tar.gz
    
3.  Change into the directory created in step 2:

    .. code-block:: bash

        cd Abjad-x.y

4.  Run the following under MacOS or Linux:

    .. code-block:: bash

        sudo python setup.py install

5.  Or run this command under Windows after starting up a command shell 
    with administrator privileges:

    .. code-block:: bash

        setup.py install

These commands will cause Python to install Abjad in your site packages
directory.  You'll then be ready to start using Abjad.


Configuring Abjad
-----------------

Abjad creates a ``~/.abjad`` directory the first time it runs.  In ``~/.abjad``
you will find a the file ``abjad.cfg``.  This is the Abjad configuration file.
You can use the Abjad configuration file to tell Abjad about your preferred PDF
file viewer, MIDI player, your preferred LilyPond language and so on.

By default, your configuration file's contents will look approximately like
this:

.. code-block:: bash

    # Abjad configuration file created by Abjad on 19 October 2013 12:30:17.
    # File is interpreted by ConfigObj and should follow ini syntax.

    # Set to the directory where all Abjad-generated files
    # (such as PDFs and LilyPond files) should be saved.
    # Defaults to $HOME.abjad/output/
    abjad_output_directory = /Users/josiah/.abjad/output

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

The configuration file is in ``ini`` syntax, so make sure to follow those
conventions when editing.