LilyPond text alignment
=======================

LilyPond provides many ways to position text.

Default alignment
-----------------

LilyPond left-aligns markup relative to the left edge of note heads by default.

::

	abjad> from abjad.tools import documentationtools


::

	abjad> staff = stafftools.RhythmicStaff('c')


::

	abjad> markuptools.Markup('XX', 'up')(staff[0])


::

	abjad> lilypond_file = documentationtools.make_text_alignment_example_lilypond_file(staff)
	abjad> show(lilypond_file)

.. image:: images/default-alignment.png


``TextScript #'self-alignment-X``
---------------------------------

Use ``#'self-alignment-X`` to left-, center- or right-align markup
relative to the left edge of note heads.

Note that changes to ``#'self-alignment-X`` do not change the fact
that markup positioning is by default relative to the left edge of note heads.

::

	abjad> staff = stafftools.RhythmicStaff('c c c')


::

	abjad> markuptools.Markup('XX', 'up')(staff[0])
	abjad> staff[0].override.text_script.self_alignment_X = 'left'
	abjad> markuptools.Markup('XX', 'up')(staff[1])
	abjad> staff[1].override.text_script.self_alignment_X = 'center'
	abjad> markuptools.Markup('XX', 'up')(staff[2])
	abjad> staff[2].override.text_script.self_alignment_X = 'right'


::

	abjad> lilypond_file = documentationtools.make_text_alignment_example_lilypond_file(staff)
	abjad> show(lilypond_file)

.. image:: images/self-alignment-x-alone.png


``TextScript #'X-offset``
-------------------------

Use ``#'X-offset`` to offset markup by some number of magic units in the horizontal direction.

Specify ``#'X-offset`` arguments as numbers like ``#2.5``.
Do not specify ``#'X-offset`` arguments as direction contstants like ``#right``.

Note that changes to ``#'X-offset`` do not change the fact
that markup positioning is by default relative to the left edge of note heads.

::

	abjad> staff = stafftools.RhythmicStaff('c c c c')


::

	abjad> markuptools.Markup('XX', 'up')(staff[0])
	abjad> staff[0].override.text_script.X_offset = 0
	abjad> markuptools.Markup('XX', 'up')(staff[1])
	abjad> staff[1].override.text_script.X_offset = 2
	abjad> markuptools.Markup('XX', 'up')(staff[2])
	abjad> staff[2].override.text_script.X_offset = 4
	abjad> markuptools.Markup('XX', 'up')(staff[3])
	abjad> staff[3].override.text_script.X_offset = 6


::

	abjad> lilypond_file = documentationtools.make_text_alignment_example_lilypond_file(staff)
	abjad> show(staff)

.. image:: images/x-offset-alone.png
