\context Score = "Custom Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 4/8
			s1 * 1/2
		}
		{
			s1 * 1/2
		}
		{
			s1 * 1/2
		}
	}
	\context CustomStaff = "Custom Staff" {
		\context CustomVoice = "Custom Voice" {
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
	}
>>