Tests
=====

Abjad includes an extensive battery of tests. 
Abjad is in a state of rapid development and extension.
Major refactoring efforts are common every six to eight months and
are likely to remain so for several years.
And yet Abjad continues to allow the creation
of complex pieces of fully notated score in the midst of these changes.
We believe this is due to the extensive coverage provided by 
the automated regression battery described in the following sections.


Automated regression?
---------------------

A battery is any collection of tests. Regression tests differ from
other types of test in that they are designed to be run again and
again during many different stages of the development process.
Regression tests help ensure that the system continues to function
correctly as developers make changes to it. An automated regression
battery is one that can be run automatically by some sort of driver with
minimal manual intervention.

Several different test drivers are now in use in the Python community.
Abjad uses `py.test <http://codespeak.net/py/dist/test/test.html>`_.
The ``py.test`` distribution is not included in the Python
standard library, so one of the first thing new contributors to Abjad
should do is download and install ``py.test``, and then run the existing
battery.


Running the battery
-------------------

Change to the directory where you have Abjad installed.
Then run ``py.test``. ::

    abjad$ py.test
    =============================== test session starts ===================================
    platform darwin -- Python 2.6.1 -- pytest-2.1.0
    collected 4235 items 

    core/LilyPondContextProxy/test/test_LilypondContextProxy___eq__.py .
    core/LilyPondContextProxy/test/test_LilypondContextProxy___repr__.py .
    core/LilyPondContextProxy/test/test_LilypondContextProxy___setattr__.py ..

    ... (many lines omitted) ...

    tools/voicetools/test/test_voicetools_iterate_semantic_voices_forward_in_expr.py .
    tools/voicetools/test/test_voicetools_iterate_voices_backward_in_expr.py .
    tools/voicetools/test/test_voicetools_iterate_voices_forward_in_expr.py .

    ============================ 4235 passed in 127.06 seconds ============================

Abjad r4629 includes 4235 tests.


Reading test output
-------------------

``py.test`` crawls the entire directory structure from which 
you call it, running tests in alphabetical order. 
``py.test`` prints the total number of tests per file in square brackets
and prints test results as a single ``.`` dot for success or else
an ``F`` for failure.


Writing tests
-------------

Project check-in standards 
ask that tests accompany all code committed to the Abjad repository. 
If you add a new function, class or method to Abjad, you should add 
a new test file for that function, class or method.
If you fix or extend an existing function, class or method,
you should find the existing test file that covers that code 
and then either add a completely new test to the test file or 
else update an existing test already present in the test file.


Test files start with ``test_``
-------------------------------

When ``py.test`` first starts up it crawls the entire directory structure
from which you call it prior to running a single test. As ``py.test``
executes this preflight work, it looks for any files beginning or ending
with the string ``test`` and then collects and alphabetizes these.
Only after making such a catalog of tests does ``py.test`` begin execution.
This collect-and-cache behavior leads to the important point about naming,
below.


Avoiding name conflicts
-----------------------

Note that the names of **test functions** must be absolutely unique
across the entire directory structure on which you call ``py.test``.
You must never share names between test functions.
For example, you must not have two tests named
``test_grob_handling_01()`` **even if both tests live in different
test files**. That is, a test named ``test_grob_handling_01()``
living in the file ``test_accidental_grob_handling.py`` and a second
test named ``test_grob_handling_01()`` living in the file
``test_notehead_grob_handling.py`` will conflict with the each
other when ``py.test`` runs. And, unfortunately, **``py.test is silent
about such conflicts when it runs**. That is, should you run ``py.test``
with the duplicate naming situation described here, what will happen
is that ``py.test`` will correctly run and report results for the 
**first** such test it finds. However, when ``py.test`` encounters
the second like-named test, ``py.test`` will incorrectly report 
cached results for the **first** test rather than the second.
The take-away is to include some sort of namespacing indicators
in every test name and not to be afraid of long test names.
The ``test_grob_handling_01()`` example given here fixes easily when
the two tests rename to ``test_accidental_grob_handling_01()`` and
``test_notehead_grob_handling_01()``.


Updating ``py.test``
--------------------

It is important periodically to update ``py.test``.

The usual command to do this is::

    $ sudo easy_install -U pytest

Note that ``pytest`` is here spelled without the intervening period.


Running ``doctest`` on the ``tools`` directory
----------------------------------------------

The Python standard library includes the ``doctest`` module as way of checking
the correctness of examples included in Python docstrings.
The module searches for instances of the Python interpreter prompt ``'>>>'`` and
executes any code that follows.
Abjad docs display the Abjad prompt ``'abjad>'`` instead of the Python prompt.
This means that all instances of the Abjad prompt must be changed to Python
prompts before running ``doctest`` on the Abjad codebase.
Three scripts in ``abjad/scr/devel`` help do this.

First change to the subdirectory of the Abjad source tree on which you'd like
to run ``doctest``. Then run these scripts::

   replace-abjad-prompts-with-python-prompts

::

   run-doctest-on-all-modules-in-tree

::

   replace-python-prompts-with-abjad-prompts

After running ``run-doctest-on-all-modules-in-tree`` you can inspect the results 
that come back from ``doctest`` and make any fixes as required.
