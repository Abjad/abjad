


Getting and installing the system
=================================



Dependencies
------------


+ Python 2.5 or 2.6
+ LilyPond 2.12 or newer.


For Abjad to install and run properly, you must already have both
Python 2.5 (or Python 2.6) and LilyPond installed in your computer.
Also, make sure that both LilyPond and Python are in your PATH. To
test this simply type 'lilypond' and 'python' in your command prompt.
If both programs run then you are good to go. Otherwise you'll have to
add the location of the executables to your PATH.

You can find Python here:
`http://www.python.org <http://www.python.org>`__

and LilyPond here:
`http://www.lilypond.org <http://www.lilypond.org>`__


Installing the official source release
--------------------------------------


#. Download the latest release `HERE <../download/index.html>`__.
#. Untar the downloaded file (e.g. `tar xzvf Abjad-NNN.tar.gz`, where
   "NNN" is the version number of the latest release).
#. Change into the directory created in step 2 (e.g. "cd Abjad-NNN").
#. If you're using Linux, Mac OS X or some other flavor of Unix, enter
   the command `sudo python setup.py install` at the shell prompt. If
   you're using Windows, start up a command shell with administrator
   privileges and run the command "setup.py install".
#.


These commands will install Abjad in your Python installation's `site-
packages` directory. Note that this requires a working internet
connection if you don't already have the Python utility "setuptools"
installed.


Note for OS X users
~~~~~~~~~~~~~~~~~~~

In order to be able to run Abjad directly from the terminal via the
`abj` command, you may need to add the python binary installation
directory to your PATH. For example, if you have Python 2.6, `abj`
would usually be placed in
'/Library/Frameworks/Python.framework/Versions/2.6/bin/abj'. Thus, you
would add '/Library/Frameworks/Python.framework/Versions/2.6/bin' to
your PATH.


Note for Linux users
~~~~~~~~~~~~~~~~~~~~

Abjad makes use of xdg-open to display PDF files using your favorite
PDF viewer. Most Linux distributions now come with xdg-utils
installed. If you do not have xdg-utils installed, download it from
`www.portland.freedsektop.org <http://portland.freedesktop.org/>`__
and install it. Alternatively you can set the PDFVIEWER environment
variable to your favorite PDF viewer.


Installing the development version
----------------------------------

If you'd like to be at the cutting edge of the Abjad development use
the following alternative:


#. Install Subversion if you don't have it already installed (enter
   'svn help' to verify this).
#. Check out Abjad's 'trunck' development like so: `svn co
   svn://128.59.116.55/abjad/trunk/ abjad-trunk`
#. Make the Python interpreter aware of Abjad. There are two ways to
   do this:

    #. Make a symlink in your Python 'site-packages' directory pointing to
       the abjad-trunk directory previously checked out via Subversion: `ln
       -s 'pwd'/abjad-trunk/abjad SITE-PACKAGES-DIR/abjad` where SITE-
       PACKAGES-DIR is the Python 'site-packages' directory. In Linux this is
       usually in /usr/lib/Python2.x/site-packages.
    #. Alternatively you can include the 'abjad-trunk' directory in your
       PYTHONPATH environment variable.
    #. You will also need to include the abjad-trunk/scr directory in your
       PATH in order to be able to run abjad directly with the 'abj' command.



`Contents <../../index.html>`__


