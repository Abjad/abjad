Installation
============


Abjad depends on Python
-----------------------

You must have Python 2.5, 2.6 or 2.7 installed to run Abjad.

Abjad does not yet support the Python 3.x series of releases.

To check the version of Python installed on your computer type the following::

    python --version

You can download different versions of Python at http://www.python.org.


Abjad depends on LilyPond
-------------------------

You must have LilyPond 2.12 or greater installed for Abjad to work properly.

You can download LilyPond at http://www.lilypond.org.

After you have installed LilyPond you should type the following to see if LilyPond
is callable from your commandline::

    lilypond --version

If LilyPond is not callable from your commandline you
should add the location of the LilyPond executable to your ``PATH``
environment variable.

If you are new to working with the commandline 
you should use Google to get a basic introduction to 
editing your profile and setting environment variables.


Installing the current packaged version of Abjad with ``easy_install``
----------------------------------------------------------------------

There are different ways to install Python packages on your computer.
One of the most direct ways is with ``easy_install``.

If you have ``easy_install`` installed on your computer then you can install
Abjad with this command::

    sudo easy_install -U abjad

Python will install Abjad in the site packages directory on your 
computer and you'll be ready to start using the system.

If you do not have ``easy_install`` installed on your computer
then you should follow the instructions below to install the current
packaged version of Abjad from the Python Package Index.


Installing the current packaged version of Abjad from the Python Package Index
------------------------------------------------------------------------------

If you do not have ``easy_install`` installed on your computer
you should follow these steps to install the current packaged 
version of Abjad from the Python Package Index:

1.  Download the current release of Abjad from 
    http://pypi.python.org/pypi/Abjad.

2.  Unarchive the downloaded file. Under MacOS and Windows you can 
    double click the archived file.

    Under Linux execute the following command with ``x.y`` replaced by 
    the current release of Abjad::

        tar xzvf Abjad-x.y.tar.gz
    
3.  Change into the directory created in step 2::

        cd Abjad-x.y

4.  Run the following under MacOS or Linux::

        sudo python setup.py install

5.  Or run this command under Windows after starting up a command shell 
    with administrator privileges::

        setup.py install

These commands will cause Python to install Abjad in your site packages directory.
You'll then be ready to start using Abjad.


After install
-------------

When first run, Abjad creates an ``.abjad`` directory in your own ``$HOME`` directory.
In ``$HOME/.abjad`` you will find the Abjad configuration file: ``config.py``.
Here you can tell Abjad about your preferred PDF file viewer, MIDI player, your preferred LilyPond language, etc.
All relevant variables have defaults that you can change to suit your needs.
In Linux, for example, you might want to set your ``pdfviewer`` to ``evince`` and your ``MIDIplayer`` to ``tiMIDIty``.

``config.py`` is a regular Python file, so you should make sure the file follows Python syntax.


Note for Linux users
--------------------

Abjad defaults to ``xdg-open`` to display PDF files using your default PDF viewer.
Most Linux distributions now come with ``xdg-utils`` installed.

If you do not have ``xdg-utils`` installed, you can download it from 
http://www.portland.freedsektop.org.

Alternatively you can set the ``pdfviewer`` variable in ``$HOME/.abjad/config``
to your favorite PDF viewer. 
