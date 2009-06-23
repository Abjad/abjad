Installation
============

Abjad 1.1 requires Python 2.5 or 2.6 and LilyPond 12.2 or newer to run.
The sections below explain how to install Python, LilyPond and Abjad.


Install Python 2.5 or 2.6
-------------------------

You may already have Python installed on your computer.
Type ``python`` at the commandline to find out. ::

   $ python

   Python 2.5.1 (r251:54863, Feb  6 2009, 19:02:12) 
   [GCC 4.0.1 (Apple Inc. build 5465)] on darwin
   Type "help", "copyright", "credits" or "license" for more information.

If Python starts, then you already have Python installed.

If Python does not start, or if you have Python 2.4 or earlier,
download a newer version of Python from http://www.python.org. Make sure to avoid Python to your ``PATH`` environment variable after install. [#f1]_


Install LilyPond 2.12 or newer
------------------------------

Abjad requires LilyPond 2.12 or newer.
To see if LilyPond is already installed on your system, 
type ``lilypond --help`` at the commandline. ::

   lilypond --help

   Usage: lilypond [OPTION]... FILE...

   Typeset music and/or produce MIDI from FILE.

   LilyPond produces beautiful music notation ...

If LilyPond starts then you already have LilyPond installed on your system.

If LilyPond does not start, download from http://www.lilypond.org.
And again make sure to add LilyPond to your ``PATH`` after install.


Install Abjad 1.1
------------------------------

It is easy to install Abjad with the Python
`setuptools <http://pypi.python.org/pypi/setuptools>`__ utility. ::

   easy_install -U abjad

If you do not have ``setuptools`` installed on your computer,
just follow the steps outlined below.

1. Download the latest release from http://pypi.python.org/pypi/Abjad.

2. Untar the downloaded file. ::

      tar xzvf Abjad-1.1.tar.gz

   The sequence ``1.1`` should be the version number of the latest release.

3. Change into the directory created in step 2. ::

      cd Abjad-1.1

4. If you're using Linux [#f2]_ or MacOS [#f3]_ you can use 
   Python to install. ::

      sudo python setup.py install

5. If you're using Windows, start up a command shell with administrator
   privileges and then use ``setup.py`` to install. ::

      setup.py install

These commands install Abjad in your Python ``site-packages`` directory. 



 
.. rubric:: Notes

.. [#f1] You can check and set the value of ``PATH`` and other 
   environment variables in many ways.
   See `this Wikipedia entry 
   <http://en.wikipedia.org/wiki/Environment_variable>`_ if you
   need examples.

.. [#f2] **Note for Linux users.**
   Abjad makes use of ``xdg-open`` to display PDF files using 
   your default PDF viewer.
   Most Linux distributions now come with ``xdg-utils`` installed. 
   If you do not have ``xdg-utils`` installed, 
   download it from http://www.portland.freedsektop.org and install.
   Alternatively you can set the ``pdfviewer`` variable in the 
   ``$HOME/.abjad/config`` file to your favorite PDF viewer. 

.. [#f3] **Note for OS X users.**  
   In order to be able to run Abjad directly from the terminal via the 
   ``abj`` command, you may need to add the Python binary 
   installation directory to your ``PATH``. 
   For example, if you have Python 2.6, ``abj`` would usually be 
   placed in ``/Library/Frameworks/Python.framework/Versions/2.6/bin/abj``. 
   Thus, you would add 
   ``/Library/Frameworks/Python.framework/Versions/2.6/bin`` to your ``PATH``.  
