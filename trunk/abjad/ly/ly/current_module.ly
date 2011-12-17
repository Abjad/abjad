\version "2.14.1"

#(define current-module-sorted
  (sort
    (ly:module->alist (current-module))
    (lambda (x y)
      (symbol<? (car x) (car y)))))


#(define (display-value key value)
  (cond
    ((number? value)
      (display (format "        '~A': ~A,\n" key value)))
    ((or (symbol? value) (string? value))
      (display (format "        '~A': '~A',\n" key value)))
    ((list? value)
      (display (format "        '~A': (~A,),\n"
        key
        (string-join (map (lambda (x) (format "'~A'" x)) value) ", "))))))


#(define (document-music-function obj-pair) 
  (let*
    ; DECLARATIONS
    ((func-name (car obj-pair))
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
        "None")))
    ; BODY
    (begin
      (display (format "    '~A': {\n" func-name))
      (display (format "        'signature': ~A,\n" signature-string))
      (display "        'type': 'ly:music-function?',\n"))
      (display "    },\n")))


#(define (document-prob obj-pair) 
  (let*
    ; DECLARATIONS
    ((prob-name (car obj-pair))
    (prob (cdr obj-pair))
    (immutables (ly:prob-immutable-properties prob))
    (mutables (ly:prob-mutable-properties prob))
    (articulation-type (ly:assoc-get 'articulation-type mutables #f))
    (name (ly:assoc-get 'name immutables #f))
    (context-type (ly:assoc-get 'context-type mutables #f))
    (span-direction (ly:assoc-get 'span-direction mutables #f))
    (text (ly:assoc-get 'text mutables #f))
    (types (ly:assoc-get 'types immutables #f)))
    ; BODY
    (begin
      (display (format "    '~A': {\n" prob-name))
      (display-value "articulation-type" articulation-type)
      (display-value "context-type" context-type)
      (display-value "name" name)
      (display-value "span-direction" span-direction)
      (display-value "text" text)
      (display (format "        'type': 'ly:prob?',\n"))
      (display-value "types" types)
      (display "    },\n"))))


#(define (document-alias obj-pair) 
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


#(define (document-other obj-pair) 
  (let*
    ((name (car obj-pair))
    (value (cdr obj-pair))
    (formatted-value
      (cond
        ((number? value) value)
        ((string? value) (format "'~A'" value))
        (else "None"))))
    ;BODY
    (begin
      (display (format "    '~A': ~A,\n" name formatted-value)))))


#(define (document-object obj-pair)
  (cond
    ((ly:music-function? (cdr obj-pair))
      (document-music-function obj-pair))
    ((ly:prob? (cdr obj-pair))
      (document-prob obj-pair))
    ((string? (cdr obj-pair))
      (document-alias obj-pair))
  (else 
    (document-other obj-pair))))


#(display "current_module = {\n")
#(for-each document-object current-module-sorted)
#(display "}")
