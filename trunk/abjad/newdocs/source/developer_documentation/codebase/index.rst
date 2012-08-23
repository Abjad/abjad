Codebase
========


How the Abjad codebase is laid out
----------------------------------

The Abjad codebase comprises twelve top-level directories. ::

   abjad$ ls
   __init__.py cfg         core        docs        interfaces  scr         tools
   book        checks      demos       exceptions  opt         templates


Of these, it is in the ``tools`` directory that the bulk of the musical
reasoning implemented in Abjad resides. ::

    abjad$ ls tools/
    __init__.py       importtools       markuptools       quantizationtools stafftools
    configurationtools          instrumenttools   mathtools         resttools         tempotools
    chordtools        intervaltreetools measuretools      schemetools       threadtools
    componenttools    iotools           timesignaturetools        scoretools        tietools
    containertools    layouttools       musicxmltools     sequencetools          tonalitytools
    contexttools      leaftools         notetools         sievetools        tuplettools
    durationtools          lilyfiletools     pitcharraytools   skiptools         verticalitytools
    gracetools        marktools         pitchtools        spannertools      voicetools


The remaining sections of this chapter cover the topics necessary
to familiarize developers coming to the project for the first time.


Removing prebuilt versions of Abjad before you check out
--------------------------------------------------------

If you'd like to be at the cutting edge of the Abjad development then
you should check out from Google Code and tell Python and your operating system about Abjad.
You can do this by following the steps below.

But before you do this you should realize that there are two ways to 
get Abjad up and running on your computer.
The first way is by downloading a compressed version of Abjad from the
`Python Package Index <http://pypi.python.org/pypi/Abjad/>`_.
You probably did this when you first discovered Abjad and started to use the system.
The second way is by following the steps below to check out a copy of
the most recent version of the Abjad repository hosted on Google Code.
If you already have a version of Abjad running on your computer 
but you haven't yet followed the steps below to check out from Google Code,
then you probably downloaded a compressed version of Abjad from the Python Package Index.

**Before you check out from Google Code you should remove all prebuilt
versions of Abjad from your machine.**
The reason you need to do this is that having both a prebuilt version of Abjad
and a Subversion-managed version of Abjad on your machine can confuse your operating
system and lead to weird results when you try to start Abjad.

You remove prebuilt versions of Abjad resident on your computer 
by finding your site packages directory and removing the so-called Abjad
'egg' that Python has installed there. After you remove
the Abjad egg from your site packages directory you will also
need to remove the ``abj``, ``abjad`` and ``abjad-book`` scripts
from ``/usr/local/bin`` or from the directory that is equivalent
to ``/usr/local/bin`` under your opearting system.

First note the version of Python you're currently running. ::

    $ python --version
    Python 2.6.1

This is important because you may have more than one version of Python
installed on your machine. (Which tends especially to be the case 
if you're running a Apple's OS X.)

Then note that the site packages directory is a part of your filesystem 
into which Python installs third-party Python packages like Abjad. 
The location of the site packages directory varies from one operating system to the next
and you may have to Google to find the exact location of the site packages
directory on your machine. Under OS X you can check ``/Library/Python/2.x/site-packages/``.
Under Linux  the site packages directory is usually ``/usr/lib/python2.x/site-packages``.

Once you've found your site packages directory you can list its contents to see if
Python has installed an Abjad egg in it. ::

    site-packages$ ls
    Abjad-2.0-py2.6.egg        Sphinx-1.0.7-py2.6.egg     py-1.3.4-py2.6.egg
    Jinja2-2.5-py2.6.egg       docutils-0.7-py2.6.egg     py-1.4.0-py2.6.egg
    Pygments-1.3.1-py2.6.egg   easy-install.pth           py-1.4.4-py2.6.egg
    README                     guppy                      pytest-2.0.0-py2.6.egg
    Sphinx-1.0.1-py2.6.egg     guppy-0.1.9-py2.6.egg-info pytest-2.1.0-py2.6.egg
    Sphinx-1.0.4-py2.6.egg     py-1.3.1-py2.6.egg

Remove any Abjad eggs Python has installed in your site packages directory.

After you've done this you should check ``/usr/local/bin`` or equivalent to see
if the ``abj``, ``abjad`` or ``abjad-book`` scripts are installed there. ::

    bin$ ls
    abj      abjad    abjad-book

Remove any of the three scripts you find installed there so that you can use
the new versions of the scripts you will download from Google Code instead. ::

    bin$ sudo rm abj*

Now proceed to the steps below to check out from Google Code.


Installing the development version
----------------------------------

Follow the steps listed above to remove prebuilt versions of Abjad from your machine.
Then follow the steps below to check out from Google Code.

1. Make sure Subversion is installed on your machine. ::
   
      svn --version

   If Subversion responds then it is already installed.
   Otherwise visit the `Subversion <http://subversion.tigris.org>`_ website.

2. Check out a copy of the main line of the Abjad codebase. ::

      svn checkout http://abjad.googlecode.com/svn/abjad/trunk abjad-trunk

3. Add the abjad trunk directory to your your ``PYTHONPATH`` environment variable. ::

      export PYTHONPATH="/path/to/abjad-trunk:"$PYTHONPATH

4. Alternatively you may symlink your Python site packages directory 
   to the abjad trunk directory. ::

      ln -s /path/to/abjad-trunk /path/to/site-package/abjad

5. Finally, add ``abjad-trunk/scr/`` to your ``PATH`` environment variable. ::

      export PATH="/path/to/abjad-trunk/scr:"$PATH

    You will then be able to run Abjad with the ``abjad`` command.

You now have a copy of the main line of the most recent version of the Abjad
repository checked out to your machine.
