\context Score = "Grouped Staves Score" <<
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
	\context StaffGroup = "Grouped Staves Staff Group" <<
		\context Staff = "Staff 1" {
			\context Voice = "Voice 1" {
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
					c'16 \< \p
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
					c'16 \f
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
		}
	>>
>>