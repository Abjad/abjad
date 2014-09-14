\version "2.15.13"
\language "english"

#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 14)

\layout {
    indent = #0
    ragged-right = ##t
    \context {
        \Score
        \override BarNumber #'transparent = ##t
        \override TimeSignature #'break-visibility = #end-of-line-invisible
        proportionalNotationDuration = #(ly:make-moment 1 45)
    }
}

\paper {
    markup-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
    system-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 10) (stretchability . 0))
}
