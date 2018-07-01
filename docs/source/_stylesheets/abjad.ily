%%% METRONOME MARK FUNCTIONS %%%

#(define-markup-command
    (abjad-metronome-mark-markup layout props
    duration-log dot-count stem-height units-per-minute)
    (number? number? number? markup?)
    (interpret-markup layout props
    #{
    \markup {
        \fontsize #-6
        \general-align #Y #DOWN
        \note-by-number #duration-log #dot-count #stem-height
        \upright =
        \hspace #-0.15
        \upright
        #units-per-minute
        \hspace #1
        }
    #}
    ))

%%% TEXT SPANNER TWEAKS %%%

abjad_start_text_span_invisible = #(
    define-music-function (parser location grob) (ly:music?)
    #{
    - \tweak dash-period 0
    - \tweak bound-details.left-broken.text ##f
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    - \tweak bound-details.right.padding 1.5
    - \tweak bound-details.right.stencil-align-dir-y #center
    $grob
    #})
