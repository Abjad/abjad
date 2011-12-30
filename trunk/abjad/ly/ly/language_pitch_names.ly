\version "2.15.23"

%%% DEFINITIONS %%%

#(define alterations '(
  (-1 . "ff")
  (-3/4 . "tqf")
  (-1/2 . "f")
  (-1/4 . "qf")
  (0 . "")
  (1/4 . "qs")
  (1/2 . "s")
  (3/4 . "tqs")
  (1 . "ss")))

#(define notenames '(
  (0 . "c")
  (1 . "d")
  (2 . "e")
  (3 . "f")
  (4 . "g")
  (5 . "a")
  (6 . "b") ))

#(define (print-language language)
  (display (format "~%    '~A': " (car language))))

#(define (print-pitch pitch-pair)
  (let*
    ; DECLARATIONS
    ((ly-pitch-name (car pitch-pair))
    (ly-pitch-obj (cdr pitch-pair))
    (ly-notename (ly:pitch-notename ly-pitch-obj))
    (ly-alteration (ly:pitch-alteration ly-pitch-obj))
    (abj-pitch-name (ly:assoc-get ly-notename notenames))
    (abj-accidental (ly:assoc-get ly-alteration alterations))
    (pitch-name (format "~A~A" abj-pitch-name abj-accidental)))
    ; BODY
    (display (format "        '~A': NamedChromaticPitchClass('~A'),\n"
      ly-pitch-name pitch-name))))

#(define handle-language (lambda (x) (begin
  (print-language x)
  (display " {\n")
  (map print-pitch (cdr x))
  (display "    },\n"))))

%%% MAIN %%%

#(begin
  (display "from abjad.tools.pitchtools import NamedChromaticPitchClass\n\n\n")
  (display (format "lilypond_version = \"~A\"\n\n" (lilypond-version)))
  (display "language_pitch_names = {")
  (map handle-language language-pitch-names)
  (display "\n}"))

