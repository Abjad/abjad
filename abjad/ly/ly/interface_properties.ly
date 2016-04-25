\version "2.19.24"

#(load "helpers.scm")

#(begin

  (define (format-interface-properties h)
    "formats the interfaces from ly:all-grob-interfaces as a Python dict"
    (string-append
     (fold (lambda (k p)
             (string-append
              p
              (format-dict-entry
               (symbol->string k)
               (format-string-list
                (sort
                 (map symbol->string
                   (filter user-property?
                           (list-ref (hashq-ref h k) 2)))
                 string<)
                4)
               4)))
       "interface_properties = {\n"
       (sort-symbol-list (hash-keys h)))
     "    }\n"))

  (display
    (string-append
      (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
      (format-interface-properties (ly:all-grob-interfaces))
      )))
