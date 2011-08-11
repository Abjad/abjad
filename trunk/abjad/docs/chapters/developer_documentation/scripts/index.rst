Scripts
=======

The ``abjad/scr/devel`` directory contains scripts for Abjad developers.
Add ``abjad/scr/devel`` to your ``PATH`` to use the scripts described below. ::

    abjad$ ls scr/devel
    abj-grep              abj-rmpycs            count-source-lines
    abj-grp                abj-update            replace-in-files


Searching the Abjad codebase with ``abj-grep``
----------------------------------------------

Abjad provides a wrapper around UNIX ``grep`` in the form of ``abj-grep``.
Use this script to recursively search the entire Abjad codebase, leaving
out non-human-readable files, files located in special ``.svn`` Subversion
subdirectories, and all files in the ``abjad/documentation`` directories.
You can run ``abj-grep`` from any directory on your system; you needn't be
in the Abjad source directories when you call ``abj-grep``. ::

    $ abj-grep 'is_assignable('

    leaf/duration.py:111:            if not durtools.is_assignable(rational):
    tempo/indication.py:67:            assert durtools.is_assignable(arg)
    tools/check/are_scalable.py:12:            if not durtools.is_assignable(candidate_duration):
    tools/durtools/is_assignable.py:5:def is_assignable(duration):
    tools/durtools/prolated_to_written.py:2:from abjad.tools.durtools.is_assignable import is_assignable
    tools/durtools/prolated_to_written.py:15:    if is_assignable(prolated_duration):
    tools/tietools/duration_change.py:28:    if durtools.is_assignable(new_written_duration):
    tools/tuplettools/contents_scale.py:30:    if durtools.is_assignable(multiplier):


Removing old ``*.pyc`` files with ``abj-rmpycs``
------------------------------------------------

See the section on ``abj-update`` below for the reasons that it is a
good idea to periodically remove the byte-compiled ``*.pyc`` files that
Python generates for its own use behind the scenes. Abjad supplies
``abj-rmpycs`` to delete all the ``*.pyc`` in the Abjad codebase, leaving
other ``*.pyc`` on your system untouched.


Updating your development copy of Abjad with ``abj-update``
-----------------------------------------------------------

The normal way of updating your working copy of a Subversion repository
is with the ``svn update`` or ``svn up`` command. You can update
your working copy of Abjad in the usual way with ``svn up``. But
Abjad supplies an ``abj-update`` script as a wrapper around the usual
Subversion update commands. In addition to updating your working copy
of Abjad, ``abj-update`` populates the ``abjad/.version`` file with
the most recent revision number of the system, and then removes all
``*.pyc`` files from your Abjad install. The benefits here are twofold.
First, Abjad adds the most recent revision number of the system to all
``.ly`` files that you generate when working with Abjad. If you do not
update the Abjad version file on a regular basis, the headers in your
Abjad-generated ``.ly`` files will list the wrong version of the system.
Second, as is the case in working with any substantial Python codebase,
it is a good idea to periodically remove the byte-compiled ``*.pyc`` files
that Python creates for its own use. The reason for this is inadvertant
name aliasing. That is, if there was previously a module named ``foo.py``
somewhere in the system and if Python had at some point imported the module
and created ``foo.pyc`` as a byprodct, this ``.pyc`` file will remain on
the filesystem even if you later decide to remove, or rename, the source
``foo.py`` module. This lead to confusion because days or weeks after
``foo.py`` has been removed, Python will still find ``foo.pyc`` and seem
to make the contents of ``foo.py`` available from beyond the grave.
Updating with ``abj-update`` takes care of these two situations.


Counting lines of code with ``count-source-lines``
--------------------------------------------------

Run ``count-source-lines`` for a count of lines of count divided between
source and test files. ::

    abjad$ count-source-lines

    source_modules: 713
    test_modules: 580

    source_lines: 25899
    test_lines: 46111

    total lines: 72010
    test-to-source ratio is 1.8 : 1

The script is directory-dependent so you can run it any the entire Abjad
codebase or any subdirectory of the codebase.


Global search-and-replace with ``replace-in-files``
---------------------------------------------------

You probably won't need to use ``replace-in-files`` very often.
But if you are making changes to Abjad that will cause some name,
such as ``FooBar``, to be globally changed everywhere in the Abjad
codebase to, say to ``foo_bar``, then you can use ``replace-in-files``
to save lots of time. ::

    $ replace-in-files --help

        Usage:

        replace-in-files DIR OLD_TEXT NEW_TEXT [CONFIRM=true/false]

        Crawl directory DIR and read every file in it recursively.
        Replace OLD_TEXT with NEW_TEXT in each file.

        Set CONFIRM to `false` to replace without prompting.


Adding new development scripts
------------------------------

If you write and then find yourself using a certain script over and over
again when you're developing new code for Abjad, consider contributing
back to the project so we can include your script in the next public
release of Abjad. Scripts in the the Abjad script directories end with
no file extension and try to be as OS-portable as possible, which
usually means writing the script in Python, rather than your operating
system's shell, and relying heavily on Python's ``os`` module.
