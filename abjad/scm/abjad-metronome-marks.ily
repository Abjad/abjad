%%% METRONOME MARK FUNCTIONS %%%

#(define-markup-command
    (abjad-metronome-mark-markup layout props
    duration-log dot-count stem-height units-per-minute)
    (number? number? number? markup?)
    (interpret-markup layout props
    #{
    \markup {
        \fontsize #-6
        \general-align #Y #down
        \note-by-number #duration-log #dot-count #stem-height
        \upright =
        \hspace #-0.15
        \upright
        #units-per-minute
        \hspace #1
    }
    #}
    )
)

#(define-markup-command
    (abjad-metronome-mark-mixed-number-markup layout props
    duration-log dot-count stem-height units-per-minute n d)
    (number? number? number? markup? markup? markup?)
    (interpret-markup layout props
    #{
    \markup {
        \fontsize #-6
        \general-align #Y #down
        \note-by-number #duration-log #dot-count #stem-height
        \upright {
            =
            \hspace #-0.15
            #units-per-minute
            \hspace #-0.15
            \raise #0.2
            \fontsize #-4
            \fraction #n #d
        }
        \hspace #1
    }
    #}
    )
)
