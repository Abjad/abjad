\version "2.14.1"

#(begin

  ; write out the Python-formatted dictionary for a music function
  (define (document-music-function obj-pair) '())

  ; write out the Python-formatted dictionary for a property object
  (define (document-prob obj-pair) '())

  ; write out the Python-formatted dictionary for an alias to a prob or function
  (define (document-alias obj-pair) '())

  ; write out information for anything else not covered above
  (define (document-other obj-pair) '())

  ; lookup the formatting function to use, based on predicates
  (define (document-object obj-pair)
    (cond
      ((ly:music-function? (cdr obj-pair))
        (document-music-function obj-pair))
      ((ly:prob? (cdr obj-pair))
        (document-prob obj-pair))
      ((string? (cdr obj-pair))
        (document-alias obj-pair))
    (else 
      (document-other obj-pair))))

  ; sort the current-module (lilypond)
  (define current-module-sorted
    (sort
      (ly:module->alist (current-module))
      (lambda (x y) (symbol<? (car x) (car y)))))

  (display "current_module = {\n")

  (for-each document-object current-module-sorted)

  (display "}")

)
