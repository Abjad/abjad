#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 16)

\layout {
    ragged-right = ##t
    indent = #0
}

\paper {
    bottom-margin = 10
    left-margin = 15
    markup-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
    system-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
    top-margin = 10
}
