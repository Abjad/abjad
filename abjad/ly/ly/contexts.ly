\version "2.19.24"

#
(load "helpers.scm")

#
(load-from-path "lily-sort")

#
  (define (context-doc context-desc)
    (let* ((name-sym (assoc-get 'context-name context-desc))
        (name (symbol->string name-sym))
        (aliases (sort 
            (map symbol->string (assoc-get 'aliases context-desc))
            ly:string-ci<?))
        (accepts (sort
            (map symbol->string (assoc-get 'accepts context-desc))
            ly:string-ci<?))
        (consists (sort
            (map symbol->string (assoc-get 'consists context-desc))
            ly:string-ci<?))
        (defaultchild (assoc-get 'default-child context-desc))
        ;;and then as strings
        (accepts-entry (format-dict-entry "accepts"
          (format-string-set (format-string-list accepts 8)) 8))
        (aliases-entry (format-dict-entry "aliases"
          (format-string-set (format-string-list aliases 8)) 8))
        (consists-entry (format-dict-entry "consists"
          (format-string-set (format-string-list consists 8)) 8)) 
        (defaultchild-entry (if defaultchild
            (format "        \"default_child\": \"~A\",\n" 
                (symbol->string defaultchild)
                )
            ""))
        (all-entries (string-append
          accepts-entry
          aliases-entry
          consists-entry
          defaultchild-entry
          )))
      (string-append
        "    \"" name "\": {\n"
        all-entries
        "        },\n")))

#
(define (all-contexts-doc)
  (let* (
    (layout-alist
      (sort (ly:output-description $defaultlayout)
        (lambda (x y) (ly:symbol-ci<? (car x) (car y)))))
    (names (sort (map symbol->string (map car layout-alist)) ly:string-ci<?))
    (contexts (map cdr layout-alist)))
  (string-join (map context-doc contexts) "")))

#
(display (string-append
  (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
  "contexts = {\n"
  (all-contexts-doc)
  "    }\n"))
