\version "2.25.16"
\include "fraction-accidental-markups.ily"
\include "general-edo-accidental-markups.ily"


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

one-quarter-flat-markup = \markup \ekmelos-five \char ##xe480

three-quarters-flat-markup = \markup \ekmelos-five \char ##xe296

three-eighths-flat-markup = \markup
    \ekmelos-five
    \combine
    \char ##xe480
    \path #0.15
      #'(
          (moveto 0.74 -0.65)
          (lineto 0.74 -1.4)
          (moveto 0.44 -0.7)
          (lineto 0.74 -1.48)
          (lineto 1.04 -0.7)
          )

seven-eighths-flat-markup = \markup
    \ekmelos-five
    \combine
    \char ##xe296
    \path #0.15
      #'(
          (moveto 0.77 -0.65)
          (lineto 0.77 -1.4)
          (moveto 0.47 -0.7)
          (lineto 0.77 -1.48)
          (lineto 1.07 -0.7)
          )
