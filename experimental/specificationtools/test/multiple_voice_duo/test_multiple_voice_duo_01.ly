\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 4/8
			s1 * 1/2
		}
		{
			\time 3/8
			s1 * 3/8
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" \with {
			\override VerticalAxisGroup #'staff-staff-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 6) (stretchability . 0))
		} <<
			\context Voice = "Voice 1-1" \with {
				\override NoteHead #'Y-offset = #0.5
				\override Stem #'direction = #up
			} {
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
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
			}
			\context Voice = "Voice 1-2" \with {
				\override NoteHead #'Y-offset = #-0.5
				\override Stem #'direction = #down
			} {
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
			}
		>>
		\context RhythmicStaff = "Staff 2" \with {
			\override VerticalAxisGroup #'staff-staff-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 6) (stretchability . 0))
		} <<
			\context Voice = "Voice 2-1" \with {
				\override NoteHead #'Y-offset = #0.5
				\override Stem #'direction = #up
			} {
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
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
			}
			\context Voice = "Voice 2-2" \with {
				\override NoteHead #'Y-offset = #-0.5
				\override Stem #'direction = #down
			} {
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #1
					c'16
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #2
					c'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					c'16 ]
				}
			}
		>>
	>>
>>