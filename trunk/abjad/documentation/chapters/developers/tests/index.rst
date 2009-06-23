Writing and running tests
=========================

Abjad includes an exetensive battery of tests. Current versions of the
system include more than 2000 tests, [#]_ all of which are important to 
help verify the correct definition of the formal model of the score
as the the system grows.

Project check-in standards ask that tests accompany all code committed 
to the Abjad repository. The exact procedures for finding and modifying
tests are explained below. But the basic summary is that you should update
one or more existing tests when you fix a bug and write one or more
entirely new tests when you add a new class, method or function.

Abjad uses `py.test <http://codespeak.net/py/dist/test/test.html>`_ to
run the entire battery. If you plan on extending Abjad, whether privately
for your own use or to commit back to the public Abjad repository, the
first thing you should do is download and install py.test and then run
the entire battery.

The remaining sections in this chapter describe how to get and run py.test,
how the Abjad tests are organized on the filesystem, how to change existing
tests, write new tests, and commit changes back to the repository.

.. todo:: Finish me.

.. rubric:: Footnotes

.. [#] Abjad r2330, for example, includes 2157 tests.
