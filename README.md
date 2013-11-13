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


Dependencies
------------

Abjad depends on the following binaries:

    * Python 2.7
    * LilyPond 2.16 or newer
    * Graphviz (optional, for documentation)

and on the following Python packages:

    * configobj
    * ply
    * pytest
    * sphinx

For Abjad to install and run properly, you must already have both Python 2.7
and LilyPond installed in your computer.

Note that Abjad does not yet support Python 3.0 or greater.

Also, make sure that both LilyPond and Python are in your PATH.

To test this simply type ...

    lilypond --version

... and then ...

    python --version

... at your command prompt. 

If both programs run then you are good to go.

Otherwise you'll have to add the location of the executables to your PATH.

You can find Python here: http://www.python.org

You can find LilyPond here: http://www.lilypond.org

You can find Graphviz here: http://graphviz.org/


Installing the latest prebuilt version of Abjad
-----------------------------------------------

If you have setuptools installed, simply type ...

    sudo easy_install -U abjad

... in the command prompt of your terminal window.

Python will install the latest prebuilt version of Abjad 
in the site packages directory on your computer and 
this will complete your installation of Abjad.

Otherwise, follow these manual install instructions:

1.  Download the latest release from http://pypi.python.org/pypi/Abjad.

2.  Untar the downloaded file. For example ...

        tar xzvf Abjad-NNN.tar.gz
    
    ... where NNN is the version number of the latest release.

3.  Change into the directory created in step 2 with ...

        cd Abjad-NNN

    ... or equivalent.

4.  If you're using Linux, Mac OS X or some other flavor of Unix, 
    enter the command ...

        sudo python setup.py install

    ... at your command prompt.

5.  If you're using Windows, start up a command shell with administrator
    privileges and run the command ...

        setup.py install

    ... at your comamnd prompt.

These commands will cause Python to install Abjad in your site packages
directory.


Note for Linux users
--------------------

Abjad defaults to xdg-open to display PDF files using your default PDF viewer.
Most Linux distributions now come with xdg-utils installed.

If you do not have xdg-utils installed, you can download it from 
http://www.portland.freedsektop.org and install it.

Alternatively you can set the pdfviewer variable in the $HOME/.abjad/abjad.cfg
file to your favorite PDF viewer. 
