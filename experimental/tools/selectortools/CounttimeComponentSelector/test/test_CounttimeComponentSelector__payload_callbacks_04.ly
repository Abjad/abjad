\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 2/4
			s1 * 1/2
		}
		{
			\time 3/8
			s1 * 3/8
		}
		{
			\time 3/4
			s1 * 3/4
		}
		{
			\time 2/4
			s1 * 1/2
		}
		{
			\time 3/8
			s1 * 3/8
		}
		{
			\time 3/4
			s1 * 3/4
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					c'16 [
					c'8
					c'8. ]
				}
				{
					c'16 [
					c'8
					c'8. ]
				}
				{
					c'16 [
					c'8
					c'8. ]
				}
				{
					c'16 [
					c'8
					c'8. ]
				}
				{
					c'16 [
					c'16 ]
				}
				{
					c'16 [
					c'8
					c'8. ]
				}
				{
					c'16 [ ]
				}
				{
					c'16 [
					c'8
					c'8. ]
				}
				{
					c'16 [ ]
				}
				{
					c'16 [
					c'8
					c'8. ]
				}
				{
					c'16 [ ]
				}
				{
					c'16 [
					c'8
					c'8 ]
				}
			}
		}
	>>
>>