Pitch overview
==============

Abjad models pitch with a combination of custom classes and helper functions.

Custom classes
--------------

Abjad implements custom :class:`Note <abjad.note.note.Note>`, :class:`Chord <abjad.chord.chord.Chord>`, :class:`NoteHead <abjad.notehead.notehead.NoteHead>`, :class:`Pitch <abjad.pitch.pitch.Pitch>` and :class:`Accidental <abjad.accidental.accidental.Accidental>` classes to model the way that notes and pitches work together.


Helper functions
----------------

Abjad implements a collection of helper functions to operate on pitch.


Microtonality
-------------

Abjad implements quartertones only.


.. note::

   The chapters here refer to both object-oriented Abjad classes and to the pitch-classes of American music theory. This first use of 'class' refers to instantiable code and the second to the residue classes of a pitch space.
   
   For the conventions these chapters follow, refer to the appendix on :doc:`pitch conventions <chapters/pitch_conventions/index>`.

.. todo::

   Implement support for LilyPond arrowed accidentals.

