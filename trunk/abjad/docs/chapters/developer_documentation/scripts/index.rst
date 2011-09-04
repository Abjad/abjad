Scripts
=======

The ``abjad/scr/devel`` directory contains scripts for Abjad developers.
Add ``abjad/scr/devel`` to your ``PATH`` to use the scripts described below. ::

    abjad$ ls scr/devel
    abj-grep                                       find-multifunction-modules
    abj-grp                                        find-multiline-import-statements
    abj-rmpycs                                     find-nonalphabetized-module-headers
    abj-src-grp                                    find-nontrivial-subdirectories
    abj-test-grp                                   find-public-helpers-without-docstrings
    abj-update                                     find-undocumented-tools
    capitalize-test-file-names                     fix-nonalphabetized-module-headers
    conjoin-multiline-import-statements            fix-test-case-block-comments
    count-source-lines                             fix-test-case-names
    count-tools                                    fix-test-case-numbers
    duplicate-test-file                            format-lilypond-context-names-with-underscores
    find-and-fix-manual-class-package-initializers list-private-modules
    find-duplicate-module-names                    rebuild-docs
    find-duplicate-tool-module-names               reindent-3-spaces-as-4
    find-import-as-statements                      reindent-4-spaces-as-3
    find-local-import-statements                   reindent-spaces-variably
    find-lower-camel-case-definitions              remove-tmp-out-directories
    find-lower-camel-case-modules                  rename-public-helper
    find-manual-class-loads-in-initializers        replace-abjad-prompts-with-python-prompts
    find-misnamed-private-modules                  replace-in-files
    find-missing-test-modules                      replace-python-prompts-with-abjad-prompts
    find-module-headers                            run-doctest-on-all-modules-in-tree
    find-modules-with-chevrons


Searching the Abjad codebase with ``abj-grep``
----------------------------------------------

Abjad provides a wrapper around UNIX ``grep`` in the form of ``abj-grep``.
Use this script to recursively search the entire Abjad codebase, leaving
out non-human-readable files, files located in special ``.svn`` Subversion
subdirectories, and all files in the ``abjad/documentation`` directories.
You can run ``abj-grep`` from any directory on your system; you needn't be
in the Abjad source directories when you call ``abj-grep``. ::

    $ abj-grep 'is_assignable('
    leaf/duration.py:111:            if not durationtools.is_assignable(rational):
    tempo/indication.py:67:            assert durationtools.is_assignable(arg)
    tools/check/are_scalable.py:12:            if not durationtools.is_assignable(candidate_duration):
    tools/durationtools/is_assignable.py:5:def is_assignable(duration):
    tools/durationtools/prolated_to_written.py:2:from abjad.tools.durationtools.is_assignable import is_assignable
    tools/durationtools/prolated_to_written.py:15:    if is_assignable(prolated_duration):
    tools/tietools/duration_change.py:28:    if durationtools.is_assignable(new_written_duration):
    tools/tuplettools/contents_scale.py:30:    if durationtools.is_assignable(multiplier):


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

    source_modules: 1703
    test_modules:   1812

    source_lines:   73942
    test_lines:     76636

    total lines:    150578
    test-to-source ratio is 1 : 1

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
