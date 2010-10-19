Glossary
========

.. glossary::

   assignability
      Attribute used of rational numbers that can be written as the 
      duration of notes and rests without recourse to ties.
      The numbers ``1/8`` and ``3/16`` are assignable while the numbers
      ``5/16`` and ``9/16`` are not.

   coverage
      The percentage of public classes, methods and functions currently
      documented in the system (doc coverage).
      Also the percentage of code exercised when the regression tests run (test coverage).

   driver
      Used in reference to the testing process the term refers to the
      application chosen to execute a collection of tests before, during
      or after making changes to the system.
      Abjad uses `py.test <http://codespeak.net/py/dist/test/test.html>`_ 
      to execute the regression battery automatically.
     
   grob
      LilyPond contraction of 'graphic object'. 
      LilyPond grobs are either 'printing' or 'nonprinting'.

   parentage
      The containment profile of any Abjad component.
      Consider a note contained within a tuplet contained within a staff.
      The 'improper' parentage of that note lists the note itself, 
      the containing tuplet and the containing staff, all in that order.
      The 'proper' parentage of that note lists only the containing tuplet
      and the containing staff.

   render
      To format an Abjad object as a PDF.
      Same as calling :func:`~abjad.tools.iotools.show`.

   thread
      Time-sequential components within a voice.
      See the chapter on :doc:`/chapters/fundamentals/threads/index` 
      for a detailed discussion.
