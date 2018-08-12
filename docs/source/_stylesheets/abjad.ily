#(ly:set-option 'relative-includes #t)
\include "abjad-text-spanner-line-styles.ily"
\include "naselnik-text-spanner-id.ily"
\include "solomon-flared-hairpin.ily"


%%% COLOR OVERRIDES %%%

abjad-color-music = #(
    define-music-function (parser location color music) (symbol? ly:music?)
    #{
    \once \override Accidental.color = #(x11-color #'color)
    \once \override Beam.color = #(x11-color #'color)
    \once \override Dots.color = #(x11-color #'color)
    \once \override Flag.color = #(x11-color #'color)
    \once \override NoteHead.color = #(x11-color #'color)
    \once \override Rest.color = #(x11-color #'color)
    \once \override Stem.color = #(x11-color #'color)
    $music
    #}
    )

%%% GLISSANDO OVERRIDES %%%

abjad-continuous-glissando = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \override Glissando.bound-details.left.padding = -1
    \override Glissando.bound-details.left.start-at-dot = ##f
    \override Glissando.bound-details.right.padding = 0
    $music
    #}
    )

abjad-revert-continuous-glissando = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \revert Glissando.bound-details.left.padding
    \revert Glissando.bound-details.left.start-at-dot
    \revert Glissando.bound-details.right.padding
    $music
    #}
    )

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
    )
    )
