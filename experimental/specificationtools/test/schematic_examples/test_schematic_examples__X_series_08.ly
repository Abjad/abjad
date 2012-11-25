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
		{
			\time 2/8
			s1 * 1/4
		}
		{
			\time 3/16
			s1 * 3/16
		}
		{
			s1 * 3/16
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #1
						c'8 [
						\set stemLeftBeamCount = #1
						\set stemRightBeamCount = #1
						c'8
						\set stemLeftBeamCount = #1
						\set stemRightBeamCount = #1
						c'8
						\set stemLeftBeamCount = #1
						\set stemRightBeamCount = #0
						c'8 ]
					}
				}
				{
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
						\set stemRightBeamCount = #2
						c'16
						\set stemLeftBeamCount = #2
						\set stemRightBeamCount = #0
						c'16 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #3
						c'32 [
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #0
						c'32 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #2
						c'16 [
						\set stemLeftBeamCount = #2
						\set stemRightBeamCount = #0
						c'16 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #3
						c'32 [
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #0
						c'32 ]
					}
				}
			}
		}
		\context RhythmicStaff = "Staff 2" {
			\context Voice = "Voice 2" {
				{
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
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #3
						c'32 [
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #0
						c'32 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #1
						c'8 [
						\set stemLeftBeamCount = #1
						\set stemRightBeamCount = #0
						c'8 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #2
						c'16 [
						\set stemLeftBeamCount = #2
						\set stemRightBeamCount = #0
						c'16 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #3
						c'32 [
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #0
						c'32 ]
					}
				}
			}
		}
		\context RhythmicStaff = "Staff 3" {
			\context Voice = "Voice 3" {
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #3
						c'32 [
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #0
						c'32 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #1
						c'8 [
						\set stemLeftBeamCount = #1
						\set stemRightBeamCount = #1
						c'8
						\set stemLeftBeamCount = #1
						\set stemRightBeamCount = #0
						c'8 ]
					}
				}
				{
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
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #2
						c'16 [
						\set stemLeftBeamCount = #2
						\set stemRightBeamCount = #0
						c'16 ]
					}
				}
				{
					{
						\set stemLeftBeamCount = #0
						\set stemRightBeamCount = #3
						c'32 [
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #3
						c'32
						\set stemLeftBeamCount = #3
						\set stemRightBeamCount = #0
						c'32 ]
					}
				}
			}
		}
		\context RhythmicStaff = "Staff 4" {
			\context Voice = "Voice 4" {
				{
					r32
					c'4..
					r32
				}
				{
					r32
					c'4 ~
					c'16
					r32
				}
				{
					r32
					c'8.
					r32
				}
				{
					r32
					c'8
					r32
				}
				{
					r32
					c'8
					r32
				}
			}
		}
	>>
>>