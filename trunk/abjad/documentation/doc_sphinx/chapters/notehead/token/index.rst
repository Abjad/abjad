Notehead token input
====================

Abjad :class:`Note <abjad.note.note.Note>` and :class:`Chord <abjad.chord.chord.Chord>` instances accept both :doc:`pitch token </chapters/pitch/token/index>` instances and Abjad :class:`NoteHead <abjad.notehead.notehead.NoteHead>` instances as input.

For example:

::

	abjad> note = Note(0, (1, 4))
	abjad> note.notehead = 13
	

.. image:: images/notehead_token1.png

Abjad groups :doc:`pitch token </chapters/pitch/token/index>` instances and Abjad :class:`NoteHead <abjad.notehead.notehead.NoteHead>` instances together under the heading of **notehead token input**.

Examples in the documentation that ask for notehead token input accept any of the input types shown here.

