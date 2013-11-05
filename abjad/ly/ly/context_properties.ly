\version "2.16.1"

#(load "helpers.scm")

#(begin

  (define (format-context-properties)
    "writes out the list of context (translation) properties"
    (string-append
     "context_properties = "
     (format-string-list
      (sort
       (map symbol->string all-user-translation-properties)
       string<)
      0)
     "\n"))

  (display
    (string-append
      (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
      (format-context-properties)
      )))

% EOF
