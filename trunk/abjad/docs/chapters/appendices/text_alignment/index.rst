LilyPond text alignment
=======================

LilyPond provides many ways to position text.

Default alignment
-----------------

LilyPond left-aligns markup relative to the left edge of note heads by default.

::

	>>> from abjad.tools import documentationtools


::

	>>> staff = stafftools.RhythmicStaff('c')


::

	>>> markuptools.Markup('XX', Up)(staff[0])


::

	>>> lilypond_file = documentationtools.make_text_alignment_example_lilypond_file(staff)
	>>> show(lilypond_file)

.. image:: images/default-alignment.png


``TextScript #'self-alignment-X``
---------------------------------

Use ``#'self-alignment-X`` to left-, center- or right-align markup
relative to the left edge of note heads.

Note that changes to ``#'self-alignment-X`` do not change the fact
that markup positioning is by default relative to the left edge of note heads.

::

	>>> staff = stafftools.RhythmicStaff('c c c')


::

	>>> markuptools.Markup('XX', Up)(staff[0])
	>>> staff[0].override.text_script.self_alignment_X = 'left'
	>>> markuptools.Markup('XX', Up)(staff[1])
	>>> staff[1].override.text_script.self_alignment_X = 'center'
	>>> markuptools.Markup('XX', Up)(staff[2])
	>>> staff[2].override.text_script.self_alignment_X = 'right'


::

	>>> lilypond_file = documentationtools.make_text_alignment_example_lilypond_file(staff)
	>>> show(lilypond_file)

.. image:: images/self-alignment-x-alone.png


``TextScript #'X-offset``
-------------------------

Use ``#'X-offset`` to offset markup by some number of magic units in the horizontal direction.

Specify ``#'X-offset`` arguments as numbers like ``#2.5``.
Do not specify ``#'X-offset`` arguments as direction contstants like ``#right``.

Note that changes to ``#'X-offset`` do not change the fact
that markup positioning is by default relative to the left edge of note heads.

::

	>>> staff = stafftools.RhythmicStaff('c c c c')


::

	>>> markuptools.Markup('XX', Up)(staff[0])
	>>> staff[0].override.text_script.X_offset = 0
	>>> markuptools.Markup('XX', Up)(staff[1])
	>>> staff[1].override.text_script.X_offset = 2
	>>> markuptools.Markup('XX', Up)(staff[2])
	>>> staff[2].override.text_script.X_offset = 4
	>>> markuptools.Markup('XX', Up)(staff[3])
	>>> staff[3].override.text_script.X_offset = 6


::

	>>> lilypond_file = documentationtools.make_text_alignment_example_lilypond_file(staff)
	>>> show(staff)

.. image:: images/x-offset-alone.png
