%%% GLISSANDO LINE STYLES %%%

abjad-zero-padding-glissando = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak bound-details.left.padding 0
    - \tweak bound-details.left.start-at-dot ##f
    - \tweak bound-details.right.padding 0
    $music
    #}
    )

%%% TEXT SPANNER LINE STYLES %%%

abjad-dashed-line-with-arrow = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak arrow-width 0.25
    - \tweak dash-fraction 0.25
    - \tweak dash-period 1.5
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.left-broken.text ##f
    - \tweak bound-details.right.arrow ##t
    - \tweak bound-details.right.padding 0.5
    - \tweak bound-details.right.stencil-align-dir-y #center
    - \tweak bound-details.right-broken.arrow ##t
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )

abjad-dashed-line-with-hook = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak dash-fraction 0.25
    - \tweak dash-period 1.5
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.left-broken.text ##f
    % right padding to avoid last leaf in spanner:
    %%%- \tweak bound-details.right.padding 1.25
    - \tweak bound-details.right.stencil-align-dir-y #up
    - \tweak bound-details.right.text \markup { \draw-line #'(0 . -1) }
    - \tweak bound-details.right-broken.arrow ##f
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )

abjad-dashed-line-with-up-hook = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak dash-fraction 0.25
    - \tweak dash-period 1.5
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.left-broken.text ##f
    % right padding to avoid last leaf in spanner:
    %%%- \tweak bound-details.right.padding 1.25
    - \tweak bound-details.right.stencil-align-dir-y #down
    - \tweak bound-details.right.text \markup { \draw-line #'(0 . -1) }
    - \tweak bound-details.right-broken.arrow ##f
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )
    
abjad-invisible-line = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak dash-period 0
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.left-broken.text ##f
    - \tweak bound-details.right.padding 0.5
    - \tweak bound-details.right.stencil-align-dir-y #center
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )
    
abjad-solid-line-with-arrow = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak arrow-width 0.25
    - \tweak dash-fraction 1
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.left-broken.text ##f
    - \tweak bound-details.right.arrow ##t
    - \tweak bound-details.right.padding 0.5
    - \tweak bound-details.right.stencil-align-dir-y #center
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )
    
abjad-solid-line-with-hook = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak dash-fraction 1
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.left-broken.text ##f
    % right padding to avoid last leaf in spanner:
    - \tweak bound-details.right.padding 1.25
    - \tweak bound-details.right.stencil-align-dir-y #up
    - \tweak bound-details.right.text \markup { \draw-line #'(0 . -1) }
    - \tweak bound-details.right-broken.arrow ##f
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )

abjad-solid-line-with-up-hook = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    - \tweak Y-extent ##f
    - \tweak dash-fraction 1
    - \tweak bound-details.left.stencil-align-dir-y #center
    - \tweak bound-details.left-broken.text ##f
    % right padding to avoid last leaf in spanner:
    - \tweak bound-details.right.padding 1.25
    - \tweak bound-details.right.stencil-align-dir-y #down
    - \tweak bound-details.right.text \markup { \draw-line #'(0 . -1) }
    - \tweak bound-details.right-broken.arrow ##f
    - \tweak bound-details.right-broken.padding 0
    - \tweak bound-details.right-broken.text ##f
    $music
    #}
    )
