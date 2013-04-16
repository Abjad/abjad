\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 2/8
			s1 * 1/4
		}
		{
			\time 2/4
			s1 * 1/2
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					\once \override Accidental #'color = #red
					\once \override Beam #'color = #red
					\once \override Dots #'color = #red
					\once \override Flag #'color = #red
					\once \override NoteHead #'color = #red
					\once \override Stem #'color = #red
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\once \override Accidental #'color = #red
					\once \override Beam #'color = #red
					\once \override Dots #'color = #red
					\once \override Flag #'color = #red
					\once \override NoteHead #'color = #red
					\once \override Stem #'color = #red
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
				{
					\once \override Accidental #'color = #red
					\once \override Beam #'color = #red
					\once \override Dots #'color = #red
					\once \override Flag #'color = #red
					\once \override NoteHead #'color = #red
					\once \override Stem #'color = #red
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\once \override Accidental #'color = #red
					\once \override Beam #'color = #red
					\once \override Dots #'color = #red
					\once \override Flag #'color = #red
					\once \override NoteHead #'color = #red
					\once \override Stem #'color = #red
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
					\set stemRightBeamCount = #0
					c'16 ]
				}
			}
		}
	>>
>>