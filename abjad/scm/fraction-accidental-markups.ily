\version "2.25.16"


#(define-markup-command
    (accidental-fraction-down-markup layout props num den)
    (markup? markup?)
    (interpret-markup layout props
    #{
    \markup
    \pad-markup #0.125
	\override #'(style . outline)
    \override #'(thickness . 0.8)
	\whiteout
    \fontsize #-4
	\bold
    \translate #'(-1 . 0.15)
	\center-column {
    #num
	\translate #'(0 . 2/3)
	#den
	\translate #'(0 . 25/16)
	\musicglyph "arrowheads.close.1M1"
	}
    #}))

#(define-markup-command
    (accidental-fraction-up-markup layout props num den)
    (markup? markup?)
    (interpret-markup layout props
    #{
    \markup
    \pad-markup #0.125
	\override #'(style . outline)
    \override #'(thickness . 0.8)
	\whiteout
    \fontsize #-4
	\bold
    \translate #'(-1 . 2)
	\center-column {
	\translate #'(0 . -1/12)
	\musicglyph "arrowheads.close.11"
    #num
	\translate #'(0 . 2/3)
	#den
	}
    #}))



one-third-sharp-markup = \markup \accidental-fraction-up-markup 1 3
two-thirds-sharp-markup = \markup \accidental-fraction-up-markup 2 3
one-third-flat-markup = \markup \accidental-fraction-down-markup 1 3
two-thirds-flat-markup = \markup \accidental-fraction-down-markup 2 3
one-sixth-sharp-markup = \markup \accidental-fraction-up-markup 1 6
five-sixths-sharp-markup = \markup \accidental-fraction-up-markup 5 6
one-sixth-flat-markup = \markup \accidental-fraction-down-markup 1 6
five-sixths-flat-markup = \markup \accidental-fraction-down-markup 5 6
one-twelfth-sharp-markup = \markup \accidental-fraction-up-markup 1 12
five-twelfths-sharp-markup = \markup \accidental-fraction-up-markup 5 12
seven-twelfths-sharp-markup = \markup \accidental-fraction-up-markup 7 12
eleven-twelfths-sharp-markup = \markup \accidental-fraction-up-markup 11 12
one-twelfth-flat-markup = \markup \accidental-fraction-down-markup 1 12
five-twelfths-flat-markup = \markup \accidental-fraction-down-markup 5 12
seven-twelfths-flat-markup = \markup \accidental-fraction-down-markup 7 12
eleven-twelfths-flat-markup = \markup \accidental-fraction-down-markup 11 12
one-fifth-sharp-markup = \markup \accidental-fraction-up-markup 1 5
two-fifths-sharp-markup = \markup \accidental-fraction-up-markup 2 5
three-fifths-sharp-markup = \markup \accidental-fraction-up-markup 3 5
four-fifths-sharp-markup = \markup \accidental-fraction-up-markup 4 5
one-fifth-flat-markup = \markup \accidental-fraction-down-markup 1 5
two-fifths-flat-markup = \markup \accidental-fraction-down-markup 2 5
three-fifths-flat-markup = \markup \accidental-fraction-down-markup 3 5
four-fifths-flat-markup = \markup \accidental-fraction-down-markup 4 5
one-tenth-sharp-markup = \markup \accidental-fraction-up-markup 1 10
three-tenths-sharp-markup = \markup \accidental-fraction-up-markup 3 10
seven-tenths-sharp-markup = \markup \accidental-fraction-up-markup 7 10
one-tenth-flat-markup = \markup \accidental-fraction-down-markup 1 10
three-tenths-flat-markup = \markup \accidental-fraction-down-markup 3 10
seven-tenths-flat-markup = \markup \accidental-fraction-down-markup 7 10
