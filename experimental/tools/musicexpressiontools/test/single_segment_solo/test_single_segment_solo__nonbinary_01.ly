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
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				\tweak #'edge-height #'(0.7 . 0)
				\times 4/5 {
					c'4
				}
				\tweak #'edge-height #'(0.7 . 0)
				\times 4/5 {
					c'4
				}
				\tweak #'edge-height #'(0.7 . 0)
				\times 4/5 {
					c'4
				}
				\tweak #'edge-height #'(0.7 . 0)
				\times 4/5 {
					c'4
				}
				\tweak #'edge-height #'(0.7 . 0)
				\times 4/5 {
					c'16.
				}
			}
		}
	>>
>>