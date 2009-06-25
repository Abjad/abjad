Glossary
========

Abjad uses the following terms in ways that are unique to the project.


.. glossary::

   assignable
      See :term:`notehead-assignable`.

   coverage
      The percentage of public classes, methods and functions currently
      documented in the system (doc coverage). Also the percentage
      of code exercised when the regression tests run (test coverage).
      Abjad coverage goals are set at 100% for the docs and as high
      as possible for the core code.
     
   format
      The LilyPond input string corresponding to an Abjad object.
      The :term:`format` of the Abjad ``Note(1, (1, 4))`` is
      ``cs'4``.

   notehead-assignable
      Rational-valued numbers like ``1/4``, ``1/8`` and ``3/16`` that
      can be written as the duration of notes and rests without recourse
      to ties. The numbers ``5/16`` and ``9/16`` require ties when written
      as the duration of a note or rest and are, therefore, *not*
      notehead-assignable.

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
