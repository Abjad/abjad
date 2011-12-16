\version "2.14.1"

#(begin

  (define current-module-sorted
    (sort
      (ly:module->alist (current-module))
      (lambda (x y)
        (symbol<? (car x) (car y)))))


  (define (document-music-function obj-pair) 
    (let*

      ; DECLARATIONS
      (

      (func-name (car obj-pair))
      (music-func (cdr obj-pair))
      (func (ly:music-function-extract music-func))
      (arg-names
        (map symbol->string 
          (cddr (cadr (procedure-source func)))))
      (signature (object-property func 'music-function-signature))
      (signature-syms (map (lambda (x) (procedure-name x)) signature))
      (signature-string
        (if (< 0 (length signature))
          (format "(~A,)" (string-join (map (lambda (x)
            (format "'~A'" x))
            signature-syms) ", "))
          "None"))
      )

      ; BODY
      (begin
        (display (format "    '~A': {\n" func-name))
        (display (format "        'signature': ~A,\n" signature-string))
        (display "        'type': 'ly:music-function?',\n"))
        (display "    },\n")))


  (define (document-prob obj-pair) 
    (let*
      ; DECLARATIONS
      ()
      ; BODY
      ()))


  (define (document-alias obj-pair) 
    (let
      ; DECLARATIONS
      ((name (car obj-pair))
      (alias (ly:assoc-get (string->symbol (cdr obj-pair)) current-module-sorted #f)))
      ; BODY
      (if alias 
        (begin
          (display (format "    '~A': {\n" name))
          (display (format "        'alias': '~A',\n" (cdr obj-pair)))
          (display (format "        'type': 'alias',\n"))
          (display "    },\n"))
        (display (format "    '~A': None,\n" name)))))


  (define (document-other obj-pair) '())


  (define (document-object obj-pair)
    (cond
      ((ly:music-function? (cdr obj-pair))
        (document-music-function obj-pair))
;      ((ly:prob? (cdr obj-pair))
;        (document-prob obj-pair))
      ((string? (cdr obj-pair))
        (document-alias obj-pair))
    (else 
      (document-other obj-pair))))


  (display "current_module = {\n")
  (for-each document-object current-module-sorted)
  (display "}"))
