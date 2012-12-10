\version "2.16.1"

#(begin

  (define (sort-symbol-list list)
    "sort a list of symbols"
    (sort list (lambda (s1 s2)
                 (string<
                  (symbol->string s1)
                  (symbol->string s2)))))
  
  (define (hash-keys h)
    "returns the list of keys of a hash table"
    (hash-fold
     (lambda (k v p)
       (append p (list k)))
     '()
     h))
  
  ;; the list of properties we also want to complete, besides all
  ;; user properties
  (define accepted-properties
    '(
      cross-staff
      positioning-done
      ))
  
  (define (user-property? prop)
    "is the property a user property?"
    (or (memq prop accepted-properties)
        (memq prop all-user-grob-properties)))
  
  (define (format-string-list list indent)
    "formats a list of strings as a python list"
    (cond
     ((null? list) "[]")
     (else 
      (string-append
       "[\n"
       (string-join
        (map (lambda (s)
               (string-append
                (make-string (+ 4 indent) #\space)
                "\""
                s
                "\",\n"))
          list)
        "")
       (make-string indent #\space)
       "]"))))
  
  (define (format-dict-entry k v indent)
    "formats a dictionary entry: key and value are string"
    (string-append
     (make-string indent #\space)
     "\"" k "\": " v ",\n"))
  
  (define (format-interfaces h)
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
       "interfaces = {\n"
       (sort-symbol-list (hash-keys h)))
     "}\n"))
  
  (define (alist-keys alist)
    "returns the list of keys of the specified alist"
    (fold 
     (lambda (l p)
       (append p (list (car l))))
     '()
     alist))
  
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
       "grobs = {\n"
       (sort-symbol-list (alist-keys all-grob-descriptions)))
     "}\n"))
  
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
     (format-string-list
      (sort (get-translator-names) string-ci<?)
      0)
     "\n"))

  (define (format-musicglyphs)
    "writes the list of music glyphs"
    (string-append
     "music_glyphs = "
     (format-string-list
      (sort
       (delete ".notdef"
         (ly:otf-glyph-list (ly:system-font-load "emmentaler-20")))
       string<)
      0)
     "\n"))
  ) 
