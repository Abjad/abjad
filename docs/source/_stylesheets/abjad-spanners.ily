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
