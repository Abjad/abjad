\version "2.25.16"

#(define-markup-command
    (heji-accidental-markup layout props point-code)
    (number?)
    (interpret-markup layout props
    #{
    \markup
    \fontsize #5
    \override #(cons 'font-name font-name)
    \char #point-code
    #}))

#(define-markup-command
    (heji-double-accidental-markup layout props point-code1 point-code2 kern)
    (number? number? number?)
    (interpret-markup layout props
    #{
    \markup
    \fontsize #5
    \override #(cons 'font-name font-name)
    \concat {
    \char #point-code1
    \hspace #kern
    \char #point-code2
    }
    #}))

#(define-markup-command
    (heji-triple-accidental-markup layout props point-code kern)
    (number? number?)
    (interpret-markup layout props
    #{
    \markup
    \fontsize #5
    \override #(cons 'font-name font-name)
    \pattern #3 #X #kern \char #point-code
    #}))

#(define-markup-command
    (letter-heji-accidental-markup layout props letter)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \fontsize #5
    \override #(cons 'font-name font-name)
    #letter
    #}))


% diatonic accidentals
abjad-natural = \markup \heji-accidental-markup ##x266e
abjad-sharp = \markup \heji-accidental-markup ##xe262
abjad-flat = \markup \heji-accidental-markup##xe260
double-sharp = \markup \heji-accidental-markup ##xe263
double-flat = \markup \heji-accidental-markup ##xe264


% natural syntonic commas
natural-one-syntonic-comma-down = \markup \heji-accidental-markup ##xe2c2
natural-two-syntonic-comma-down = \markup \heji-accidental-markup ##xe2cc
natural-three-syntonic-comma-down = \markup \heji-accidental-markup ##xe2d6
natural-one-syntonic-comma-up = \markup \heji-accidental-markup ##xe2c7
natural-two-syntonic-comma-up = \markup \heji-accidental-markup ##xe2d1
natural-three-syntonic-comma-up = \markup \heji-accidental-markup ##xe2db
% sharp syntonic commas
sharp-one-syntonic-comma-down = \markup \heji-accidental-markup ##xe2c3
sharp-two-syntonic-comma-down = \markup \heji-accidental-markup ##xe2cd
sharp-three-syntonic-comma-down = \markup \heji-accidental-markup ##xe2d7
sharp-one-syntonic-comma-up = \markup \heji-accidental-markup ##xe2c8
sharp-two-syntonic-comma-up = \markup \heji-accidental-markup ##xe2d2
sharp-three-syntonic-comma-up = \markup \heji-accidental-markup ##xe2dc
% flat syntonic commas
flat-one-syntonic-comma-down = \markup \heji-accidental-markup ##xe2c1
flat-two-syntonic-comma-down = \markup \heji-accidental-markup ##xe2cb
flat-three-syntonic-comma-down = \markup \heji-accidental-markup ##xe2d5
flat-one-syntonic-comma-up = \markup \heji-accidental-markup ##xe2c6
flat-two-syntonic-comma-up = \markup \heji-accidental-markup ##xe2d0
flat-three-syntonic-comma-up = \markup \heji-accidental-markup ##xe2da
% double sharp syntonic commas
double-sharp-one-syntonic-comma-down = \markup \heji-accidental-markup ##xe2c4
double-sharp-two-syntonic-comma-down = \markup \heji-accidental-markup ##xe2ce
double-sharp-three-syntonic-comma-down = \markup \heji-accidental-markup ##xe2d8
double-sharp-one-syntonic-comma-up = \markup \heji-accidental-markup ##xe2c9
double-sharp-two-syntonic-comma-up = \markup \heji-accidental-markup ##xe2d3
double-sharp-three-syntonic-comma-up = \markup \heji-accidental-markup ##xe2dd
% double flat syntonic commas
double-flat-one-syntonic-comma-down = \markup \heji-accidental-markup ##xe2c0
double-flat-two-syntonic-comma-down = \markup \heji-accidental-markup ##xe2ca
double-flat-three-syntonic-comma-down = \markup \heji-accidental-markup ##xe2d4
double-flat-one-syntonic-comma-up = \markup \heji-accidental-markup ##xe2c5
double-flat-two-syntonic-comma-up = \markup \heji-accidental-markup ##xe2cf
double-flat-three-syntonic-comma-up = \markup \heji-accidental-markup ##xe2d9


% septimal commas % check vertical kerning in ekmelos
one-septimal-comma-down = \markup \heji-accidental-markup ##xe2de
two-septimal-comma-down = \markup \heji-accidental-markup ##xe2e0
three-septimal-comma-down = \markup \heji-double-accidental-markup ##xe2de ##xe2e0 #0.125
one-septimal-comma-up = \markup \heji-accidental-markup ##xe2df
two-septimal-comma-up = \markup \heji-accidental-markup ##xe2e1
three-septimal-comma-up = \markup \heji-double-accidental-markup ##xe2df ##xe2e1 #0.125


% undecimal quarter tones
one-undecimal-quarter-tone-down = \markup \heji-accidental-markup ##xe2e2
two-undecimal-quarter-tone-down = \markup \heji-double-accidental-markup ##xe2e2 ##xe2e2 #0.035
three-undecimal-quarter-tone-down = \markup \heji-triple-accidental-markup ##xe2e2 #0.035

one-undecimal-quarter-tone-up = \markup \heji-accidental-markup ##xe2e3
two-undecimal-quarter-tone-up = \markup \heji-double-accidental-markup ##xe2e3 ##xe2e3 #0.125
three-undecimal-quarter-tone-up = \markup \heji-triple-accidental-markup ##xe2e3 #0.125


% tridecimal third tones
one-tridecimal-third-tone-down = \markup \heji-accidental-markup ##xe2e4
two-tridecimal-third-tone-down = \markup \heji-double-accidental-markup ##xe2e4 ##xe2e4 #0.035
three-tridecimal-third-tone-down = \markup \heji-triple-accidental-markup ##xe2e4 #0.035
one-tridecimal-third-tone-up = \markup \heji-accidental-markup ##xe2e5
two-tridecimal-third-tone-up = \markup \heji-double-accidental-markup ##xe2e5 ##xe2e5 #0.125
three-tridecimal-third-tone-up = \markup \heji-triple-accidental-markup ##xe2e5 #0.125


% seventeen-limit schismas
one-seventeen-limit-schisma-down = \markup \heji-accidental-markup ##xe2e6
two-seventeen-limit-schisma-down = \markup \heji-double-accidental-markup ##xe2e6 ##xe2e6 #0.125
three-seventeen-limit-schisma-down = \markup \heji-triple-accidental-markup ##xe2e6 #0.125
one-seventeen-limit-schisma-up = \markup \heji-accidental-markup ##xe2e7
two-seventeen-limit-schisma-up = \markup \heji-double-accidental-markup ##xe2e7 ##xe2e7 #0.125
three-seventeen-limit-schisma-up = \markup \heji-triple-accidental-markup ##xe2e7 #0.125


% nineteen-limit schismas
one-nineteen-limit-schisma-down = \markup \heji-accidental-markup ##xe2e8
two-nineteen-limit-schisma-down = \markup \heji-double-accidental-markup ##xe2e8 ##xe2e8 #0.125
three-nineteen-limit-schisma-down = \markup \heji-triple-accidental-markup ##xe2e8 #0.125
one-nineteen-limit-schisma-up = \markup \heji-accidental-markup ##xe2e9
two-nineteen-limit-schisma-up = \markup \heji-double-accidental-markup ##xe2e9 ##xe2e9 #0.125
three-nineteen-limit-schisma-up = \markup \heji-triple-accidental-markup ##xe2e9 #0.125


% twenty-three-limit commas
one-twenty-three-limit-comma-down = \markup \heji-accidental-markup ##xe2eb
two-twenty-three-limit-comma-down = \markup \heji-double-accidental-markup ##xe2eb ##xe2eb #0.125
three-twenty-three-limit-comma-down = \markup \heji-triple-accidental-markup ##xe2eb #0.125
one-twenty-three-limit-comma-up = \markup \heji-accidental-markup ##xe2ea
two-twenty-three-limit-comma-up = \markup \heji-double-accidental-markup ##xe2ea ##xe2ea #0.125
three-twenty-three-limit-comma-up = \markup \heji-triple-accidental-markup ##xe2ea #0.125
