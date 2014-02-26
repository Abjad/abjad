\header {
	tagline = \markup { "" }
}

\score {
	\new Score <<
		\new RhythmicStaff {
			{
				\time 4/16
				c'16 [
				c'16
				c'8 ]
			}
			{
				\time 2/10
				\scaleDurations #'(4 . 5) {
					c'8 [
					c'8 ]
				}
			}
			{
				\time 3/20
				\scaleDurations #'(4 . 5) {
					c'8 [
					c'16 ]
				}
			}
			{
				\time 4/16
				c'8. [
				c'16 ]
			}
			{
				\time 4/16
				c'8. [
				c'16 ]
			}
			{
				\time 11/30
				\scaleDurations #'(8 . 15) {
					c'16 [
					c'16
					c'8
					c'8.
					c'4 ]
				}
			}
			{
				\time 15/30
				\scaleDurations #'(8 . 15) {
					c'8 [
					c'16
					c'8
					c'8.
					c'4
					c'16
					c'16
					c'16 ]
				}
			}
			{
				\time 2/8
				c'8 [
				c'8 ]
			}
			{
				\time 10/26
				\scaleDurations #'(8 . 13) {
					c'8 [
					c'8.
					c'4
					c'16 ]
				}
			}
			{
				\time 4/30
				\scaleDurations #'(8 . 15) {
					c'16 [
					c'16
					c'16
					c'16 ]
				}
			}
			{
				\time 15/30
				\scaleDurations #'(8 . 15) {
					c'16 [
					c'4
					c'16
					c'16
					c'8
					c'8.
					c'16
					c'8 ]
				}
			}
			{
				\time 7/26
				\scaleDurations #'(8 . 13) {
					c'16 [
					c'4
					c'16
					c'16 ]
				}
			}
			{
				\time 3/26
				\scaleDurations #'(8 . 13) {
					c'16 [
					c'16
					c'16 ]
				}
			}
			{
				\time 1/4
				c'4 [ ]
			}
			{
				\time 10/19
				\scaleDurations #'(16 . 19) {
					c'8. [
					c'4
					c'16
					c'16
					c'16 ]
				}
			}
			{
				\time 6/26
				\scaleDurations #'(8 . 13) {
					c'16 [
					c'16
					c'4 ]
				}
			}
			{
				\time 6/20
				\scaleDurations #'(4 . 5) {
					c'4 [
					c'16
					c'16 ]
				}
			}
			{
				\time 2/20
				\scaleDurations #'(4 . 5) {
					c'16 [
					c'16 ]
				}
			}
			{
				\time 9/19
				\scaleDurations #'(16 . 19) {
					c'16 [
					c'4
					c'16
					c'16
					c'8 ]
					\bar "|."
				}
			}
		}
	>>
}