\version "2.25.16"

%{

  LilyPond includes a \flared-hairpin command. The length of the flares created
  by LilyPond's built-in \flared-hairpin command vary (very slightly) with the
  total length of the hairpin.

  The \abjad-flared-hairpin command defined here creates fixed-width flares;
  these do not vary as a function of total hairpin length.

  The \elbowed-hairpin function is included in LilyPond and was originally
  implemented by Mike Solomon. The fixed-width calculations included here were
  inspired by a post Aaron Hill made on the LilyPond user list on 2019-11-17.

%}

abjad-flared-hairpin = #(lambda (grob)
     (let* ((sten (ly:hairpin::print grob))
            (xex (ly:stencil-extent sten X))
            (yex (ly:stencil-extent sten Y))
            (width (interval-length xex))
            (height (/ (interval-length yex) 2))
            (x (- 1 (/ 0.25 width)))
            (y (* -1 (- 1 (/ 1 height)))))
       (elbowed-hairpin `((0 . 0) (,x . ,y) (1 . 1)) #t)))
