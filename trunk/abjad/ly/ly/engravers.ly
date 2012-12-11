\version "2.16.1"

\include "helpers.ly"

#(begin

  (define (get-translator-names)
    "returns the list of names of all engravers"
    (map
     (lambda (t)
       (symbol->string
        (ly:translator-name t)))
     (ly:get-all-translators)))

  (define (format-translators)
    "writes the list of engravers and performers"
    (string-append
      "engravers = "
      (format-string-set
        (format-string-list
          (sort (get-translator-names) string-ci<?)
          0))
      "\n"))

  (display
    (string-append
      (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
      (format-translators)
      )))

% EOF
