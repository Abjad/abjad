\version "2.25.16"

% FROM DAVID NALESNIK:
%
% http://lilypond.1069038.n5.nabble.com/So-slashed-beamed-grace-notes-td152817.html
%
% Implements slash command to slash run of beamed notes:
%
%    \slash

slash = { 
  $(remove-grace-property 'Voice 'Stem 'direction) 
  \once \override Stem.stencil = 
  #(lambda (grob) 
    (let* ((x-parent (ly:grob-parent grob X)) 
           (is-rest? (ly:grob? (ly:grob-object x-parent 'rest)))) 
     (if is-rest? 
      empty-stencil 
      (let* ((dir (ly:grob-property grob 'direction)) 
             (stem (ly:stem::print grob)) 
             (stem-y (ly:grob-extent grob grob Y)) 
             (stem-length (- (cdr stem-y) (car stem-y))) 
             (corr (if (= dir 1) (car stem-y) (cdr stem-y)))) 
       (ly:stencil-add 
        stem 
        (grob-interpret-markup grob 
         (markup #:translate (cons -0.5 (+ corr (* dir (1- (/ stem-length 1.1))))) 
          #:draw-line (cons 1.9 (* dir 1.7))))))))) 
} 
