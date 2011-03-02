LilyPond equivalencies in Abjad
===============================

Turning on proportional notation
--------------------------------

Turn on proportional notation like this:

::

	abjad> score = Score([ ])
	abjad> score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 24)
	abjad> score.override.spacing_spanner.uniform_stretching = True
	abjad> score.override.spacing_spanner.strict_note_spacing = True


To produce LilyPond input that looks like this:

::

	abjad> f(score)
	\new Score \with {
		\override SpacingSpanner #'strict-note-spacing = ##t
		\override SpacingSpanner #'uniform-stretching = ##t
		proportionalNotationDuration = #(ly:make-moment 1 24)
	} <<
	>>

