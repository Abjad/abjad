\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 6/8
			s1 * 3/4
		}
		{
			\time 3/8
			s1 * 3/8
		}
		{
			s1 * 3/8
		}
		{
			\time 6/8
			s1 * 3/4
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
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
					c'4 ~
					c'16
				}
				{
					c'16
				}
				{
					c'16
				}
				{
					c'16 ~
					c'4
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
			}
		}
		\context RhythmicStaff = "Staff 2" {
			\context Voice = "Voice 2" {
				{
					c'4 ~
					c'16
				}
				{
					c'4 ~
					c'16
				}
				{
					c'8
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
				{
					c'16 ~
					c'4
				}
				{
					c'16 ~
					c'4
				}
			}
		}
		\context RhythmicStaff = "Staff 3" {
			\context Voice = "Voice 3" {
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
					c'4 ~
					c'16
				}
				{
					c'4
				}
				{
					c'4
				}
				{
					c'16 ~
					c'4
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
			}
		}
		\context RhythmicStaff = "Staff 4" {
			\context Voice = "Voice 4" {
				{
					c'4 ~
					c'16
				}
				{
					c'4
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
					c'8.
				}
				{
					c'8.
				}
				{
					c'4
				}
				{
					c'16 ~
					c'4
				}
			}
		}
	>>
>>