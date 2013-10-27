\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 2/8
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
		{
			s1 * 1/4
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					c'8.
				}
				{
					\once \override Accidental #'color = #red
					\once \override Beam #'color = #red
					\once \override Dots #'color = #red
					\once \override Flag #'color = #red
					\once \override NoteHead #'color = #red
					\once \override Stem #'color = #red
					c'8.
				}
				{
					c'8.
				}
				{
					c'8.
				}
				{
					c'8.
				}
				{
					c'8.
				}
				{
					c'8
				}
			}
		}
		\context RhythmicStaff = "Staff 2" {
			\context Voice = "Voice 2" {
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
				{
					\once \override Accidental #'color = #blue
					\once \override Beam #'color = #blue
					\once \override Dots #'color = #blue
					\once \override Flag #'color = #blue
					\once \override NoteHead #'color = #blue
					\once \override Stem #'color = #blue
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\once \override Accidental #'color = #blue
					\once \override Beam #'color = #blue
					\once \override Dots #'color = #blue
					\once \override Flag #'color = #blue
					\once \override NoteHead #'color = #blue
					\once \override Stem #'color = #blue
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\once \override Accidental #'color = #blue
					\once \override Beam #'color = #blue
					\once \override Dots #'color = #blue
					\once \override Flag #'color = #blue
					\once \override NoteHead #'color = #blue
					\once \override Stem #'color = #blue
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\once \override Accidental #'color = #blue
					\once \override Beam #'color = #blue
					\once \override Dots #'color = #blue
					\once \override Flag #'color = #blue
					\once \override NoteHead #'color = #blue
					\once \override Stem #'color = #blue
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\once \override Accidental #'color = #blue
					\once \override Beam #'color = #blue
					\once \override Dots #'color = #blue
					\once \override Flag #'color = #blue
					\once \override NoteHead #'color = #blue
					\once \override Stem #'color = #blue
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
			}
		}
	>>
>>