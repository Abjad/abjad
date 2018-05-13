Using ``ajv``
=============

Abjad ships with an extensive collection of developer tools. The tools are
accessible through the ``ajv`` developer suite.

You'll find ``ajv`` in the ``abjad/scr/`` directory. Make sure to add that
directory to your path if you want to work with ``ajv``.

The ``ajv`` developer suite implements a command-line interface that is largely
self-documenting:

..  code-block:: bash

    abjad$ ajv --help
    usage: abj-dev [-h] [--version]
                
                {help,list,api,book,clean,count,doctest,grep,new,re,rename,replace,svn,test,up}
                ...

    Entry-point to Abjad developer scripts catalog.

    optional arguments:
    -h, --help            show this help message and exit

    subcommands:
    {help,list,api,book,clean,count,doctest,grep,new,re,rename,replace,svn,test,up}
        help                print subcommand help
        list                list subcommands
        api                 Build the Abjad APIs.
        book                Preprocess HTML, LaTeX or ReST source with Abjad.
        clean               Clean *.pyc, *.swp, __pycache__ and tmp*
        count               "count"-related subcommands
        doctest             Run doctests on all modules in current path.
        grep                grep PATTERN in PATH
        new                 "new"-related subcommands
        re                  Run pytest -x, doctest -x and then rebuild the API
        rename              Rename public modules.
        replace             "replace"-related subcommands
        svn                 "svn"-related subcommands
        test                Run "pytest" on various Abjad paths.
        up                  run `ajv svn up -R -C`

You can explore the different ``ajv`` subcommands like this:

..  code-block:: bash

    abjad$ ajv clean --help
    usage: clean [-h] [--version] [--pyc] [--pycache] [--swp] [--tmp] [path]

    Clean *.pyc, *.swp, __pycache__ and tmp* files and folders from PATH.

    positional arguments:
    path        directory tree to be recursed over

    optional arguments:
    -h, --help  show this help message and exit
    --pyc       delete *.pyc files
    --pycache   delete __pycache__ folders
    --swp       delete Vim *.swp file
    --tmp       delete tmp* folders


Searching the Abjad codebase with ``ajv grep``
----------------------------------------------

Abjad provides a wrapper around UNIX ``grep`` in the form of ``ajv grep``:

..  code-block:: bash

    $ ajv grep is_assignable
    ./Duration/Duration.py:361:        if not self.is_assignable:
    ./Duration/Duration.py:403:        while not candidate.is_assignable:
    ./Duration/Duration.py:477:        while not candidate.is_assignable:
    ./Duration/Duration.py:621:    def is_assignable(self):
    ./Duration/Duration.py:629:            ...         duration.is_assignable)
    ./Duration/Duration.py:654:                if mathtools.is_assignable_integer(self.numerator):
    ./Duration/Duration.py:671:        if not self.is_assignable:

Use this script to recursively search the entire Abjad codebase, leaving out
non-human-readable files, files located in special ``.svn`` Subversion
subdirectories, and all files in the ``abjad/documentation`` directories.  

You can run ``ajv grep`` from any directory on your system; you needn't be in
the Abjad source directories when you call ``ajv grep``.

Alternatively you may prefer to install ``ack`` on your system.


Removing old files with ``ajv clean``
-------------------------------------

See the section on ``ajv update`` below for the reasons that it is a good idea
to periodically remove the byte-compiled ``*.pyc`` files that Python generates
for its own use behind the scenes. Abjad supplies ``ajv clean`` to delete all
the ``*.pyc`` in the Abjad codebase, leaving other ``*.pyc`` on your system
untouched.


Updating your development copy of Abjad with ``ajv up``
-------------------------------------------------------

The normal way of updating your working copy of a Subversion repository is with
the ``svn update`` or ``svn up`` command. You can update your working copy of
Abjad in the usual way with ``svn up``. But Abjad supplies an ``ajv up``
command as a wrapper around the usual Subversion update commands.

In addition to updating your working copy of Abjad, ``ajv up`` populates the
``abjad/_version.py`` file with the most recent revision number of the system,
and then removes all ``*.pyc`` files from your Abjad install. The benefits here
are twofold.  First, Abjad adds the most recent revision number of the system
to all ``.ly`` files that you generate when working with Abjad. If you do not
update the Abjad version file on a regular basis, the headers in your
Abjad-generated ``.ly`` files will list the wrong version of the system.
Second, as is the case in working with any substantial Python codebase, it is a
good idea to periodically remove the byte-compiled ``*.pyc`` files that Python
creates for its own use. The reason for this is inadvertant name aliasing. That
is, if there was previously a module named ``foo.py`` somewhere in the system
and if Python had at some point imported the module and created ``foo.pyc`` as
a byprodct, this ``.pyc`` file will remain on the filesystem even if you later
decide to remove, or rename, the source ``foo.py`` module. This lead to
confusion because days or weeks after ``foo.py`` has been removed, Python will
still find ``foo.pyc`` and seem to make the contents of ``foo.py`` available
from beyond the grave.

Updating with ``ajv up`` takes care of these two situations.


Counting classes and functions with ``ajv count``
-------------------------------------------------

You can use ``ajv count tools .`` on the ``abjad/tools/`` directory
to get a count of classes and functions:

..  code-block:: bash

    tools$ ajv count tools .
    PUBLIC FUNCTIONS:  465
    PUBLIC CLASSES:    486
    PRIVATE FUNCTIONS: 38
    PRIVATE CLASSES:   0


Global search-and-replace with ``ajv replace``
----------------------------------------------

You probably won't need to use ``ajv replace`` very often.  But if you are
making changes to Abjad that will cause some name, such as ``FooBar``, to be
globally changed everywhere in the Abjad codebase to, say to ``foo_bar``, then
you can use ``ajv replace`` to save lots of time:

..  code-block:: bash

    $ ajv replace text . 'FooBar' 'foo_bar' -Y
