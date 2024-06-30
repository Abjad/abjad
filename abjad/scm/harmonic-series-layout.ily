\version "2.25.16"

\layout
{
  indent = #1
  ragged-last = ##t
  ragged-right = ##t
  \accidentalStyle dodecaphonic
  \override Beam.transparent = ##t
  \override Stem.transparent = ##t
  \override Staff.BarLine.stencil = ##f
  \override Flag.transparent = ##t
  \override Staff.TimeSignature.stencil = ##f
  \override SpacingSpanner.strict-grace-spacing = ##t
  \override SpacingSpanner.uniform-stretching = ##t
  \override SpacingSpanner.strict-note-spacing = ##t
  \override SpacingSpanner.uniform-stretching = ##t
  \context
  {
      \Score
      proportionalNotationDuration = \musicLength 1*1/30
  }
}
