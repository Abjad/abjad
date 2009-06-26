Glossary
========

Abjad uses the following terms in ways that are unique to the project.


.. glossary::

   altitude
      Attribute of pitches equal to the integer number of staff spaces 
      above middle C at which a pitch notates on the grand staff.
      The altitude of middle C is zero. Used as a measure of the
      absolute height of a pitch.
      
   assignable
      Attribute used of rational numbers that can be written as the 
      duration of notes and rests without recourse to ties.
      The numbers ``1/4``, ``1/8`` and ``3/16`` are assignable.
      The numbers ``5/16`` and ``9/16`` are not assignable.

   coverage
      The percentage of public classes, methods and functions currently
      documented in the system (doc coverage). Also the percentage
      of code exercised when the regression tests run (test coverage).
      Abjad coverage goals are set at 100% for the docs and as high
      as possible for the core code.

   driver
      Used in reference to the testing process the term refers to the
      application chosen to execute a collection of tests before, during
      or after making changes to the system. Abjad uses 
      `py.test <http://codespeak.net/py/dist/test/test.html>`_ 
      to execute the regression battery automatically.
     
   format
      LilyPond input string corresponding to an Abjad object.

   render
      Short-hand verb meaning to format an Abjad object as valid LilyPond
      input and then pass that input to LilyPond to create a PDF of
      the resulting notation. The same as calling :func:`~abjad.tools.io.show` 
      on an Abjad object.

   thread
      A term referring to a structural relationship binding a strictly 
      sequential set of :class:`~abjad.voice.voice.Voice` level Abjad
      component. See the chapter on :doc:`/chapters/fundamentals/threads/index` 
      for a detail discussion.
