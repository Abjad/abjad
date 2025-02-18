\version "2.25.16"


abjad-natural-markup = \markup
    \musicglyph "accidentals.natural"

abjad-sharp-markup = \markup
    \musicglyph "accidentals.sharp"

abjad-flat-markup = \markup
    \musicglyph "accidentals.flat"

double-sharp-markup = \markup
    \musicglyph "accidentals.doublesharp"

double-flat-markup = \markup
    \musicglyph "accidentals.flatflat"

one-quarter-sharp-markup = \markup
    \musicglyph "accidentals.sharp.slashslash.stem"

three-quarters-sharp-markup = \markup
    \musicglyph "accidentals.sharp.slashslash.stemstemstem"

one-eighth-sharp-markup = \markup
    \combine
    \musicglyph "accidentals.natural"
    \path #0.15
      #'(
          (moveto -0.22 0.9)
          (lineto 0.08 1.7)
          (lineto 0.38 0.9)
          )

three-eighths-sharp-markup = \markup
    \combine
    \musicglyph "accidentals.sharp.slashslash.stem"
    \path #0.15
      #'(
          (moveto 0.35 1.15)
          (lineto 0.35 2.0)
          (moveto 0.05 1.2)
          (lineto 0.35 2.0)
          (lineto 0.65 1.2)
          )

five-eighths-sharp-markup = \markup
    \combine
    \musicglyph "accidentals.sharp"
    \path #0.15
      #'(
          (moveto 0.8 1.15)
          (lineto 0.8 2.0)
          (moveto 0.5 1.2)
          (lineto 0.8 2.0)
          (lineto 1.1 1.2)
          )

seven-eighths-sharp-markup = \markup
    \combine
    \musicglyph "accidentals.sharp.slashslash.stemstemstem"
    \path #0.15
      #'(
          (moveto 1.25 1.15)
          (lineto 1.25 2.0)
          (moveto 0.95 1.2)
          (lineto 1.25 2.0)
          (lineto 1.55 1.2)
          )

one-eighth-flat-markup = \markup
    \combine
    \musicglyph "accidentals.natural"
    \path #0.15
      #'(
          (moveto 0.6 -0.95)
          (lineto 0.6 -1.7)
          (moveto 0.3 -1)
          (lineto 0.6 -1.78)
          (lineto 0.9 -1)
          )

five-eighths-flat-markup = \markup
    \combine
    \musicglyph "accidentals.flat"
    \path #0.15
      #'(
          (moveto 0.03 -0.65)
          (lineto 0.03 -1.4)
          (moveto -0.29 -0.7)
          (lineto 0.03 -1.48)
          (lineto 0.33 -0.7)
          )
