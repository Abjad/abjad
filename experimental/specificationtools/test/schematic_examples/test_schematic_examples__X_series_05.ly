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
			\time 1/8
			s1 * 1/8
		}
		{
			s1 * 1/8
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					c'32 [
					c'16
					c'16. ]
				}
				{
					c'32 [
					c'16
					c'16. ]
				}
				{
					c'32 [
					c'16
					c'16. ]
				}
				{
					c'32 [
					c'16
					c'16. ]
				}
				{
					c'32 [
					c'16
					c'16. ]
				}
				{
					c'32 [
					c'16
					c'16. ]
				}
			}
		}
		\context RhythmicStaff = "Staff 2" {
			\context Voice = "Voice 2" {
				{
					c'16 [
					c'16.
				}
				{
					c'32 ]
				}
				{
					c'16 [
					c'16.
				}
				{
					c'32 ]
				}
				{
					c'16 [
					c'16.
				}
				{
					c'32 ]
				}
				{
					c'16 [
					c'16.
				}
				{
					c'32 ]
				}
				{
					c'16 [
					c'16.
				}
				{
					c'32 ]
				}
				{
					c'16 [
					c'16.
				}
				{
					c'32 ]
				}
			}
		}
		\context RhythmicStaff = "Staff 3" {
			\context Voice = "Voice 3" {
				{
					c'32 [
					c'16.
				}
				{
					c'32
					c'32 ]
				}
				{
					c'32 [
					c'16.
				}
				{
					c'32
					c'32 ]
				}
				{
					c'32 [
					c'16.
				}
				{
					c'32
					c'32 ]
				}
				{
					c'32 [
					c'16.
				}
				{
					c'32
					c'32 ]
				}
				{
					c'32 [
					c'16.
				}
				{
					c'32
					c'32 ]
				}
				{
					c'32 [
					c'16.
				}
				{
					c'32
					c'32 ]
				}
			}
		}
		\context RhythmicStaff = "Staff 4" {
			\context Voice = "Voice 4" {
				{
					c'16. [
				}
				{
					c'32
					c'16 ]
				}
				{
					c'16. [
				}
				{
					c'32
					c'16 ]
				}
				{
					c'16. [
				}
				{
					c'32
					c'16 ]
				}
				{
					c'16. [
				}
				{
					c'32
					c'16 ]
				}
				{
					c'16. [
				}
				{
					c'32
					c'16 ]
				}
				{
					c'16. [
				}
				{
					c'32
					c'16 ]
				}
			}
		}
	>>
>>