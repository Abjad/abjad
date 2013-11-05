\version "2.16.1"



#
  (load "helpers.scm")

#
  (load-from-path "lily-sort")

#
  (define name->engraver-table (make-hash-table 61))

#
  (map
    (lambda (x)
      (hash-set! name->engraver-table (ly:translator-name x) x))
    (ly:get-all-translators))

#
  (define (find-engraver-by-name name)
    "NAME is a symbol."
    (hash-ref name->engraver-table name #f
    ))

#
  (define (engraver-grobs grav)
    (let* ((eg (if (symbol? grav)
           (find-engraver-by-name grav)
           grav)))
      (if (eq? eg #f
      )
      '()
      (map symbol->string (assoc-get 'grobs-created (ly:translator-description eg))))))

#
  (define (context-grobs context-desc)
    (let* ((group (assq-ref context-desc 'group-type))
        (consists (append
          (if group
            (list group)
            '())
          (assoc-get 'consists context-desc)))
        (grobs  (apply append
          (map engraver-grobs consists))))
      grobs))

#
  (define (context-doc context-desc)
    (let* ((name-sym (assoc-get 'context-name context-desc))
        (name (symbol->string name-sym))
        (aliases  (map symbol->string (assoc-get 'aliases context-desc)))
        (accepts  (map symbol->string (assoc-get 'accepts context-desc)))
        (consists (map symbol->string (assoc-get 'consists context-desc)))
        ;;(props    (map symbol->string (map car (map cdr (assoc-get 'property-ops context-desc)))))
        (grobs    (context-grobs context-desc))
        ;;and then as strings
        (accepts-entry (format-dict-entry "accepts"
          (format-string-set (format-string-list accepts 8)) 8))
        (aliases-entry (format-dict-entry "aliases"
          (format-string-set (format-string-list aliases 8)) 8))
        (consists-entry (format-dict-entry "consists"
          (format-string-set (format-string-list consists 8)) 8)) 
        (grobs-entry (format-dict-entry "grobs"
          (format-string-set (format-string-list grobs 8)) 8))
        ;;(props-entry (format-dict-entry "props"
        ;;  (format-string-set (format-string-list props 8)) 8))
        (all-entries (string-append
          accepts-entry
          aliases-entry
          consists-entry
          grobs-entry
          ;;props-entry
          )))
      (string-append
        "    \"" name "\": {\n"
        all-entries
        "    },\n")))

#
  (define (all-contexts-doc)
    (let* ((layout-alist
          (sort (ly:output-description $defaultlayout)
            (lambda (x y) (ly:symbol-ci<? (car x) (car y)))))
        (names (sort (map symbol->string (map car layout-alist)) ly:string-ci<?))
        (contexts (map cdr layout-alist)))
    (string-join  
      (map context-doc contexts)
      "")))

#
  (display (string-append
    (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
    "contexts = {\n"
    (all-contexts-doc)
    "}\n"))
