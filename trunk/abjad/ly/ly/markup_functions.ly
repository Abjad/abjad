\version "2.15.23"


#(define (markup-function? func)
  (and (markup-command-signature func)
    (not (object-property func 'markup-list-command))))


#(define (markup-list-function? func)
  (and (markup-command-signature func)
    (object-property func 'markup-list-command)))


#(define (sort-procedures procs)
  (sort procs
    (lambda (x y)
      (symbol<? (procedure-name x) (procedure-name y)))))


#(define (strip-procedure-suffix proc)
  (let
    ((proc-name (symbol->string (procedure-name proc))))
    (cond
      ((markup-function? proc)
        (substring proc-name 0 (string-contains proc-name "-markup")))
      ((markup-list-function? proc)
        (substring proc-name 0 (string-contains proc-name "-markup-list"))))))


#(define (document-procedure proc)
  (let*
    ((proc-name (strip-procedure-suffix proc))
    (signature (object-property proc 'markup-signature))
    (signature-syms (map (lambda (x) (procedure-name x)) signature))
    (signature-string
      (if (< 0 (length signature))
        (format "[~A]" (string-join (map (lambda (x)
          (format "'~A'" x))
          signature-syms) ", "))
        "[ ]")))
    (display (format "    '~A': ~A,\n" proc-name signature-string))))


#(define all-markup-functions (sort-procedures
  (filter procedure?
    (flatten-list
      (map (lambda (x) (hash-table->alist (cdr x)))
        (hash-table->alist markup-functions-by-category))))))


#(define all-markup-list-functions (map car (hash-table->alist markup-list-functions)))


#(display (format "lilypond_version = \"~A\"\n\n" (lilypond-version)))
#(display "markup_functions = {\n")
#(map document-procedure all-markup-functions)
#(display "}\n\n")
#(display "markup_list_functions = {\n")
#(map document-procedure all-markup-list-functions)
#(display "}\n")
