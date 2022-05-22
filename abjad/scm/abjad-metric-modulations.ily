\include "abjad-make-music-functions.ily"
\include "abjad-metronome-marks.ily"


#(define-markup-command
    (abjad-bracketed-metric-modulation layout props
        mm-length mm-dots mm-stem mm-value
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale)
    (number? number? number? string?
        number? number? number? number?
        pair?)
    (interpret-markup layout props
    #{
    \markup {
        \concat {
            \abjad-metronome-mark-markup #mm-length #mm-dots #mm-stem #mm-value
            \hspace #2
            \upright [
            \abjad-metric-modulation
                #lhs-length #lhs-dots #rhs-length #rhs-dots
                #modulation-scale
            \hspace #0.5
            \upright ]
        }
    }
    #})
    )

#(define-markup-command
    (abjad-bracketed-mixed-number-metric-modulation layout props
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale)
    (number? number? number? string? string? string?
        number? number? number? number?
        pair?)
    (interpret-markup layout props
    #{
    \markup {
        \concat {
            \abjad-metronome-mark-mixed-number-markup
                #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d 
            \hspace #2
            \upright [
            \abjad-metric-modulation
                #lhs-length #lhs-dots #rhs-length #rhs-dots
                #modulation-scale
            \hspace #0.5
            \upright ]
        }
    }
    #})
    )

#(define-markup-command
    (abjad-bracketed-metric-modulation-tuplet-lhs layout props
        mm-length mm-dots mm-stem mm-value
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale)
    (number? number? number? string?
        number? number? number? number?
        number? number?
        pair?)
    (interpret-markup layout props
    #{
    \markup {
        \concat {
            \abjad-metronome-mark-markup #mm-length #mm-dots #mm-stem #mm-value
            \hspace #2
            \upright [
            \abjad-metric-modulation-tuplet-lhs
                #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
                #note-length #note-dots
                #modulation-scale
            \hspace #0.5
            \upright ]
        }
    }
    #})
    )

#(define-markup-command
    (abjad-bracketed-mixed-number-metric-modulation-tuplet-lhs layout props
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale)
    (number? number? number? string? string? string?
        number? number? number? number?
        number? number?
        pair?)
    (interpret-markup layout props
    #{
    \markup {
        \concat {
            \abjad-metronome-mark-mixed-number-markup
                #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            \hspace #2
            \upright [
            \abjad-metric-modulation-tuplet-lhs
                #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
                #note-length #note-dots
                #modulation-scale
            \hspace #0.5
            \upright ]
        }
    }
    #})
    )

#(define-markup-command
    (abjad-bracketed-metric-modulation-tuplet-rhs layout props
        mm-length mm-dots mm-stem mm-value
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale)
    (number? number? number? string?
        number? number?
        number? number? number? number?
        pair?)
    (interpret-markup layout props
    #{
    \markup {
        \concat {
            \abjad-metronome-mark-markup #mm-length #mm-dots #mm-stem #mm-value
            \hspace #2
            \upright [
            \abjad-metric-modulation-tuplet-rhs
                #note-length #note-dots
                #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
                #modulation-scale
            \hspace #0.5
            \upright ]
        }
    }
    #})
    )

#(define-markup-command
    (abjad-bracketed-mixed-number-metric-modulation-tuplet-rhs layout props
        mm-length mm-dots mm-stem mm-base mm-n mm-d
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale)
    (number? number? number? string? string? string?
        number? number?
        number? number? number? number?
        pair?)
    (interpret-markup layout props
    #{
    \markup {
        \concat {
            \abjad-metronome-mark-mixed-number-markup
                #mm-length #mm-dots #mm-stem #mm-base #mm-n #mm-d
            \hspace #2
            \upright [
            \abjad-metric-modulation-tuplet-rhs
                #note-length #note-dots
                #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
                #modulation-scale
            \hspace #0.5
            \upright ]
        }
    }
    #})
    )

% TODO: abstract out score building code to separate function
#(define-markup-command
    (abjad-metric-modulation layout props
        lhs-length lhs-dots rhs-length rhs-dots modulation-scale)
    (number? number? number? number? pair?)
    (interpret-markup layout props
    #{
    \markup {
        \scale #modulation-scale {
            \score
                {
                    \new Score
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = #0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \new RhythmicStaff
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = #5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = #4
                            \override TupletBracket.padding = #1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = #0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            \abjad-make-note #lhs-length #lhs-dots
                        }
                    >>
                    \layout {
                        indent = #0
                        ragged-right = ##t
                    }
                }
            =
            \hspace #-0.5
            \score
                {
                    \new Score
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = #0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \new RhythmicStaff
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = #5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = #4
                            \override TupletBracket.padding = #1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = #0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            \abjad-make-note #rhs-length #rhs-dots
                        }
                    >>
                    \layout {
                        indent = #0
                        ragged-right = ##t
                    }
                }
            }
        }
    #})
    )

% TODO: abstract out score building code to separate function
#(define-markup-command
    (abjad-metric-modulation-tuplet-lhs layout props
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale)
    (number? number? number? number?
        number? number?
        pair?)
    (interpret-markup layout props
    #{
    \markup {
        \scale #modulation-scale {
            \score
                {
                    \new Score
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = #0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \new RhythmicStaff
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = #5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = #4
                            \override TupletBracket.padding = #1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = #0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            \abjad-make-tuplet-monad #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
                        }
                    >>
                    \layout {
                        indent = #0
                        ragged-right = ##t
                    }
                }
            =
            \hspace #-0.5
            \score
                {
                    \new Score
                    \with
                    {
                        \override SpacingSpanner.spacing-increment = #0.5
                        proportionalNotationDuration = ##f
                    }
                    <<
                        \new RhythmicStaff
                        \with
                        {
                            \remove Time_signature_engraver
                            \remove Staff_symbol_engraver
                            \override Stem.direction = #up
                            \override Stem.length = #5
                            \override TupletBracket.bracket-visibility = ##t
                            \override TupletBracket.direction = #up
                            \override TupletBracket.minimum-length = #4
                            \override TupletBracket.padding = #1.25
                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                            \override TupletNumber.font-size = #0
                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                            tupletFullLength = ##t
                        }
                        {
                            \abjad-make-note #note-length #note-dots
                        }
                    >>
                    \layout {
                        indent = #0
                        ragged-right = ##t
                    }
                }
            }
        }
    #})
    )

% TODO: abstract out score building code to separate function
#(define-markup-command
    (abjad-metric-modulation-tuplet-rhs layout props
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale
        )
    (number? number?
        number? number? number? number?
        pair?
        )
    (interpret-markup layout props
    #{
    \markup {
        \scale #modulation-scale
        {
        \score
            {
                \new Score
                \with
                {
                    \override SpacingSpanner.spacing-increment = #0.5
                    proportionalNotationDuration = ##f
                }
                <<
                    \new RhythmicStaff
                    \with
                    {
                        \remove Time_signature_engraver
                        \remove Staff_symbol_engraver
                        \override Stem.direction = #up
                        \override Stem.length = #5
                        \override TupletBracket.bracket-visibility = ##t
                        \override TupletBracket.direction = #up
                        \override TupletBracket.minimum-length = #4
                        \override TupletBracket.padding = #1.25
                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                        \override TupletNumber.font-size = #0
                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                        tupletFullLength = ##t
                    }
                    {
                        \abjad-make-note #note-length #note-dots
                    }
                >>
                \layout {
                    indent = #0
                    ragged-right = ##t
                }
            }
        =
        \hspace #-0.5
        \score
            {
                \new Score
                \with
                {
                    \override SpacingSpanner.spacing-increment = #0.5
                    proportionalNotationDuration = ##f
                }
                <<
                    \new RhythmicStaff
                    \with
                    {
                        \remove Time_signature_engraver
                        \remove Staff_symbol_engraver
                        \override Stem.direction = #up
                        \override Stem.length = #5
                        \override TupletBracket.bracket-visibility = ##t
                        \override TupletBracket.direction = #up
                        \override TupletBracket.minimum-length = #4
                        \override TupletBracket.padding = #1.25
                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                        \override TupletNumber.font-size = #0
                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                        tupletFullLength = ##t
                    }
                    {
                        \abjad-make-tuplet-monad #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
                    }
                >>
                \layout {
                    indent = #0
                    ragged-right = ##t
                }
            }
        }
        }
    #})
    )
