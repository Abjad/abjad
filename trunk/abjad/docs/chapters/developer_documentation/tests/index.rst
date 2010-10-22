Tests
=====

Abjad includes an extensive battery of tests. 
Abjad is in a state of rapid development and extension.
Major refactoring efforts are common every six to eight months, and
are likely to remain so at least 2012.
And yet Abjad continues to allow the creation
of complex pieces of fully notated score in the midst of these changes.
We believe this is due to the extensive coverage provided by 
the automated regression battery described in the following sections. [#]_


Automated regression?
---------------------

A battery is any collection of tests. Regression tests differ from
other types of test in that they are designed to be run again and
again during many different stages of the development process.
Regression tests help ensure that the system continues to function
correctly as we make changes to it. An automated regression
battery is one that can be run automatically by some sort of driver with
minimal manual intervention.

Several different test drivers are now in use in the Python community.
Of these, Abjad uses `py.test <http://codespeak.net/py/dist/test/test.html>`_.
The ``py.test`` distribution is not included in the Python
standard library, so one of the first thing new contributors to Abjad
should do is download and install ``py.test``, and then run the existing
battery.


Running the battery
-------------------

Change to the directory where you have Abjad installed. 
Then run ``py.test``. ::

   abjad$ py.test
   ============================= test process starts ==============================
   executable:   /Library/Frameworks/Python.framework/Versions/2.5/Resources/Python
   .app/Contents/MacOS/Python  (2.5.0-final-0)
   using py lib: /Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/sit
   e-packages/py <rev unknown>

   accidental/test/test_accidental_compare.py[3] ...
   accidental/test/test_accidental_eq.py[3] ...
   accidental/test/test_accidental_init.py[2] ..
   accidental/test/test_accidental_interface_grob_handling.py[2] ..
   accidental/test/test_accidental_interface_style.py[2] ..

   ... (many lines omitted) ...

   tuplet/test/test_tuplet_number_grob_handling.py[3] ...
   update/test/test_update_interface.py[10] ..........
   voice/interface/test/test_voice_interface_explicit.py[2] ..
   voice/interface/test/test_voice_interface_number.py[5] .....
   voice/test/test_voice_len.py[2] ..

   ================ tests finished: 2165 passed in 232.53 seconds =================


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

.. note:: The names of **test functions** must be absolutely unique
   across the entire directory structure on which you call ``py.test``.
   You must never share names between test functions.
   For example, you must not have two tests named
   ``test_grob_handling_01( )`` **even if both tests live in different
   test files**. That is, a test named ``test_grob_handling_01( )``
   living in the file ``test_accidental_grob_handling.py`` and a second
   test named ``test_grob_handling_01( )`` living in the file
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
   The ``test_grob_handling_01( )`` example given here fixes easily when
   the two tests rename to ``test_accidental_grob_handling_01( )`` and
   ``test_notehead_grob_handling_01( )``.


.. rubric:: Footnotes

.. [#] Abjad r2371 includes 2165 tests.
