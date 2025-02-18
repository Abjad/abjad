\version "2.25.16"
\include "fraction-accidental-markups.ily"
\include "general-et-accidental-markups.ily"

% one quarter tone down
one-quarter-flat-markup = \markup \musicglyph "accidentals.mirroredflat"

% three quarter tones down
three-quarters-flat-markup = \markup \musicglyph "accidentals.mirroredflat.flat"

% three eighth tones down
three-eighths-flat-markup = \markup
    \combine
    \musicglyph "accidentals.mirroredflat"
    \path #0.15
      #'(
          (moveto 0.6 -0.65)
          (lineto 0.6 -1.4)
          (moveto 0.3 -0.7)
          (lineto 0.6 -1.48)
          (lineto 0.9 -0.7)
          )

% seven eighth tones down
seven-eighths-flat-markup = \markup
    \combine
    \musicglyph "accidentals.mirroredflat.flat"
    \path #0.15
      #'(
          (moveto 0.79 -0.65)
          (lineto 0.79 -1.4)
          (moveto 0.49 -0.7)
          (lineto 0.79 -1.48)
          (lineto 1.09 -0.7)
          )
