\version "2.19.24"

#(load "helpers.scm")

#(begin

  (define (format-grob-interfaces)
    "writes out all grob interfaces as a Python dict"
    (string-append
     (fold (lambda (k p)
             (string-append
              p
              (format-dict-entry
               (symbol->string k)
               (format-string-list
                (sort
                 (map symbol->string
                   (assq-ref
                    (assq-ref
                     (assq-ref all-grob-descriptions k)
                     'meta)
                    'interfaces))
                 string<)
                4)
               4)))
       "grob_interfaces = {\n"
       (sort-symbol-list (alist-keys all-grob-descriptions)))
     "    }\n"))

  (display
    (string-append
      (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
      (format-grob-interfaces)
      )))
