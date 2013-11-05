Tests
=====

Abjad includes an extensive battery of tests.  Abjad is in a state of rapid
development and extension.  Major refactoring efforts are common every six to
eight months and are likely to remain so for several years.  And yet Abjad
continues to allow the creation of complex pieces of fully notated score in the
midst of these changes.  We believe this is due to the extensive coverage
provided by the automated regression battery described in the following
sections. Abjad 2.13 includes more than 10,000 tests.


Automated regression?
---------------------

A battery is any collection of tests. Regression tests differ from other types
of test in that they are designed to be run again and again during many
different stages of the development process.  Regression tests help ensure that
the system continues to function correctly as developers make changes to it. An
automated regression battery is one that can be run automatically by some sort
of driver with minimal manual intervention.

Several different test drivers are now in use in the Python community.  Abjad
uses `pytest <http://codespeak.net/py/dist/test/test.html>`_.  The ``pytest``
distribution is not included in the Python standard library, so one of the
first thing new contributors to Abjad should do is download and install
``pytest``, and then run the existing battery.


Running the battery
-------------------

Change to the directory where you have Abjad installed.
Then run ``pytest``:

..  code-block:: bash

    abjad$ pytest
    ============================= test session starts ==============================
    platform darwin -- Python 2.7.3 -- pytest-2.3.4
    collected 4361 items / 3 skipped 

    demos/desordre/test/test_demos_desordre.py .
    demos/ferneyhough/test/test_demos_ferneyhough.py .
    demos/mozart/test/test_demos_mozart.py .
    demos/part/test/test_demos_part.py .
    demos/part/test/test_demos_part_create_pitch_contour_reservoir.py .
    demos/part/test/test_demos_part_durate_pitch_contour_reservoir.py .
    demos/part/test/test_demos_part_shadow_pitch_contour_reservoir.py .
    ly/test/test_ly_environment.py .
    tools/abctools/AbjadObject/test/test_AbjadObject___repr__.py ..
    tools/scoretools/Chord/test/test_Chord___contains__.py ..
    tools/scoretools/Chord/test/test_Chord___copy__.py .....
    tools/scoretools/Chord/test/test_Chord___deepcopy__.py .
    ...
    ...
    ...
    tools/scoretools/Tuplet/test/test_Tuplet_toggle_prolation.py ..
    tools/scoretools/Voice/test/test_Voice___copy__.py ..
    tools/scoretools/Voice/test/test_Voice___delitem__.py .
    tools/scoretools/Voice/test/test_Voice___len__.py ..
    tools/scoretools/Voice/test/test_Voice___setattr__.py .
    tools/scoretools/Voice/test/test_Voice_is_nonsemantic.py ...
    tools/scoretools/Voice/test/test_lily_voice_resolution.py ....

    =================== 4359 passed, 5 skipped in 147.13 seconds ===================

Abjad 2.13 includes 4359 ``pytest`` tests.


Reading test output
-------------------

``pytest`` crawls the entire directory structure from which you call it,
running tests in alphabetical order.  ``pytest`` prints the total number of
tests per file in square brackets and prints test results as a single ``.`` dot
for success or else an ``F`` for failure.


Writing tests
-------------

Project check-in standards ask that tests accompany all code committed to the
Abjad repository.  If you add a new function, class or method to Abjad, you
should add a new test file for that function, class or method.  If you fix or
extend an existing function, class or method, you should find the existing test
file that covers that code and then either add a completely new test to the
test file or else update an existing test already present in the test file.


Test files start with ``test_``
-------------------------------

When ``pytest`` first starts up it crawls the entire directory structure from
which you call it prior to running a single test. As ``pytest`` executes this
preflight work, it looks for any files beginning or ending with the string
``test`` and then collects and alphabetizes these.  Only after making such a
catalog of tests does ``pytest`` begin execution.  This collect-and-cache
behavior leads to the important point about naming, below.


Avoiding name conflicts
-----------------------

Note that the names of **test functions** must be absolutely unique across the
entire directory structure on which you call ``pytest``.  You must never share
names between test functions.  For example, you must not have two tests named
``test_grob_handling_01()`` **even if both tests live in different test
files**. That is, a test named ``test_grob_handling_01()`` living in the file
``test_accidental_grob_handling.py`` and a second test named
``test_grob_handling_01()`` living in the file
``test_notehead_grob_handling.py`` will conflict with the each other when
``pytest`` runs. And, unfortunately, **pytest is silent about such
conflicts when it runs**.

That is, should you run ``pytest`` with the duplicate naming situation
described here, what will happen is that ``pytest`` will correctly run and
report results for the first such test it finds.  However, when ``pytest``
encounters the second like-named test, ``pytest`` will incorrectly report
cached results for the first test rather than the second.

The take-away is to include some sort of namespacing indicators in every test
name and not to be afraid of long test names.  The ``test_grob_handling_01()``
example given here fixes easily when the two tests rename to
``test_accidental_grob_handling_01()`` and
``test_notehead_grob_handling_01()``.


Updating ``pytest``
--------------------

It is important periodically to update ``pytest``.

The usual command to do this is:

..  code-block:: bash

    $ sudo pip install --upgrade pytest

Note that ``pytest`` is here spelled without the intervening period.


Running ``doctest`` on the ``tools`` directory
----------------------------------------------

The Python standard library includes the ``doctest`` module as way of checking
the correctness of examples included in Python docstrings.

You can use the Abjad ``ajv`` developer suite to run ``doctest`` anywhere in
the codebase:

..  code-block:: bash

    abjad$ ajv doctest
    Total modules: 954

Output like that shown above indicates that all doctests pass; errors will
print to the terminal.

Abjad 2.13 includes more than 7000 doctests.
