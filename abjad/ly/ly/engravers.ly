\version "2.19.24"

#
(load-from-path "lily-sort")

#
(load "helpers.scm")

#
(define name->engraver-table (make-hash-table 61))

#
(for-each
  (lambda (x)
    (hash-set! name->engraver-table (ly:translator-name x) x))
      (ly:get-all-translators))

#
(define (get-all-translator-names)
  (sort-symbol-list
    (map ly:translator-name (ly:get-all-translators))))

#
(define (find-engraver-by-name name)
  (hash-ref name->engraver-table name #f))

#
(define (get-grobs-created engraver)
  (map symbol->string 
    (sort-symbol-list
      (assoc-get 'grobs-created (ly:translator-description engraver)))))

#
(define (get-properties-read engraver)
  (map symbol->string
    (sort-symbol-list
      (assoc-get 'properties-read (ly:translator-description engraver)))))

#
(define (get-properties-written engraver)
  (map symbol->string
    (sort-symbol-list
      (assoc-get 'properties-written (ly:translator-description engraver)))))

#
(define (format-engraver-info engraver-name-symbol)
  (let* (
    (engraver (find-engraver-by-name engraver-name-symbol))
    (name (symbol->string engraver-name-symbol))
    (grobs-created-entry
      (format-dict-entry "grobs_created"
        (format-string-set (format-string-list (get-grobs-created engraver) 8)) 
        8))
    (properties-read-entry
      (format-dict-entry "properties_read"
        (format-string-set 
            (format-string-list (get-properties-read engraver) 8)) 
            8))
    (properties-written-entry
      (format-dict-entry "properties_written"
        (format-string-set 
            (format-string-list (get-properties-written engraver) 8)) 
            8))
    (all-entries (string-append
      grobs-created-entry
      properties-read-entry
      properties-written-entry
      )))
  (string-append
    "    \"" name "\": {\n"
    all-entries
    "    },\n")))

#
(display
  (string-append
    (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
    "engravers = {\n"
    (string-join (map format-engraver-info (get-all-translator-names)) "")
    "    }\n"))
