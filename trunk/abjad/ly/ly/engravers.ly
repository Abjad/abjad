\version "2.16.1"

\include "helpers.ly"

#(begin

  (define (format-translators)
    "writes the list of engravers and performers"
    (string-append
     "engravers = "
     (format-string-list
      (sort (get-translator-names) string-ci<?)
      0)
     "\n"))

  (display
    (string-append
      (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
      (format-translators)
      )))

% EOF
