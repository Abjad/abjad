#(ly:set-option 'relative-includes #t)
font-name = "ekmelos"
\include "markup-functions.ily"


#(define-markup-command
    (ekmelos-five layout props markup)
    (markup?)
    (interpret-markup layout props
    #{
    \markup
    \fontsize #5
    \override #'(font-name . "ekmelos")
    #markup
    #}))

% tempered accidentals %
tempered-double-flat = \markup
    \combine
    \musicglyph #"accidentals.flatflat"
    \path #0.15
      #'(
          (moveto 0.4 1.85)
          (lineto 0.65 1.85)
          (lineto 0.9 1.85)
          )


tempered-three-quarters-flat = \markup
    \ekmelos-five
    \combine
    \char ##xe296
    \path #0.15
      #'(
          (moveto 0.53 1.85)
          (lineto 0.78 1.85)
          (lineto 1.03 1.85)
          )

tempered-flat = \markup
    \combine
    \musicglyph #"accidentals.flat"
    \path #0.15
      #'(
          (moveto -0.25 1.85)
          (lineto 0 1.85)
          (lineto 0.25 1.85)
          )

tempered-quarter-flat = \markup
    \ekmelos-five
    \combine
    \char ##xe480
    \path #0.15
      #'(
          (moveto 0.53 1.85)
          (lineto 0.78 1.85)
          (lineto 1.03 1.85)
          )

tempered-natural = \markup
    \combine
    \musicglyph #"accidentals.natural"
    \path #0.15
      #'(
          (moveto -0.18 1.5)
          (lineto 0.07 1.5)
          (lineto 0.32 1.5)
          )

tempered-quarter-sharp = \markup
    \combine
    \musicglyph #"accidentals.sharp.slashslash.stem"
    \path #0.15
      #'(
          (moveto 0.1 1.25)
          (lineto 0.35 1.25)
          (lineto 0.6 1.25)
          )

tempered-sharp = \markup
    \combine
    \musicglyph #"accidentals.sharp"
    \path #0.15
      #'(
          (moveto 0.55 1.5)
          (lineto 0.8 1.5)
          (lineto 1.05 1.5)
          )

tempered-three-quarters-sharp = \markup
    \combine
    \musicglyph #"accidentals.sharp.slashslash.stemstemstem"
    \path #0.15
      #'(
          (moveto 1 1.5)
          (lineto 1.25 1.5)
          (lineto 1.5 1.5)
          )

tempered-double-sharp = \markup
    \combine
    \musicglyph #"accidentals.doublesharp"
    \path #0.15
      #'(
          (moveto 0.5 0)
          (lineto 0.5 1.05)
          (moveto 0.25 1.05)
          (lineto 0.5 1.05)
          (lineto 0.75 1.05)
          )
