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
					cs'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					d'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					ef'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					e'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					f'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					fs'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					g'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					af'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					a'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					bf'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					b'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					c'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					cs'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					d'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					ef'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					e'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					f'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					fs'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					g'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					af'16 ]
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #2
					a'16 [
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #2
					bf'16
					\set stemLeftBeamCount = #2
					\set stemRightBeamCount = #0
					b'16 ]
				}
			}
		}
	>>
>>