(begin

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
    "formats a list of strings as a Python list"
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
       "    ]"))))
  
  (define (format-string-set list)
    "format a string-list as a Python set"
    (string-append
      "set("
      list 
      ")"))

  (define (format-dict-entry k v indent)
    "formats a dictionary entry: key and value are string"
    (string-append
     (make-string indent #\space)
     "\"" k "\": " v ",\n"))
  
  (define (alist-keys alist)
    "returns the list of keys of the specified alist"
    (fold 
     (lambda (l p)
       (append p (list (car l))))
     '()
     alist))
  ) 