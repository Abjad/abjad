#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 16)

\layout {
    ragged-right = ##t
    indent = #0
    \context { \Score
        autoBeaming = ##f
        proportionalNotationDuration = #(ly:make-moment 1 24)
        tupletFullLength = ##t
        \override BarNumber #'transparent = ##t
        \override SpacingSpanner #'strict-grace-spacing = ##t
        \override SpacingSpanner #'uniform-stretching = ##t
        \override TimeSignature #'break-visibility = #end-of-line-invisible
        \override TupletBracket #'padding = #2.25
        \override TupletNumber #'text = #tuplet-number::calc-fraction-text
    }
}

\paper {
    bottom-margin = 10
    left-margin = 15
    markup-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
    system-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
    top-margin = 10
}
