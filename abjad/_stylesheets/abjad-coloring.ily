%%% COLORED MUSIC %%%

abjad-color-music = #(
    define-music-function (parser location color music) (symbol? ly:music?)
    #{
    \once \override Accidental.color = #(x11-color #'color)
    \once \override Beam.color = #(x11-color #'color)
    \once \override Dots.color = #(x11-color #'color)
    \once \override Flag.color = #(x11-color #'color)
    \once \override MultiMeasureRest.color = #(x11-color #'color)
    \once \override NoteHead.color = #(x11-color #'color)
    \once \override RepeatTie.color = #(x11-color #'color)
    \once \override Rest.color = #(x11-color #'color)
    \once \override Stem.color = #(x11-color #'color)
    \once \override StemTremolo.color = #(x11-color #'color)
    $music
    #}
    )

abjad-invisible-music = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \once \override Accidental.transparent = ##t
    \once \override Dots.transparent = ##t
    \once \override MultiMeasureRest.transparent = ##t
    \once \override NoteHead.no-ledgers = ##t
    \once \override NoteHead.transparent = ##t
    \once \override RepeatTie.transparent = ##t
    \once \override Stem.transparent = ##t
    \once \override StemTremolo.transparent = ##t
    $music
    #}
    )

abjad-invisible-music-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'salmon
    $music
    #}
    )
