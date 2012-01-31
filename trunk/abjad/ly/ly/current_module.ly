\version "2.15.23"


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
    (signature (object-property func 'music-function-signature))
    (car-signature-syms (list
      (if (pair? (car signature))
        (procedure-name (car (car signature)))
        (procedure-name (car signature)))))
    (cdr-signature-syms (flatten-list (map (lambda (x)
      (if (pair? x)
        (cons "optional?" (procedure-name (car x)))
        (procedure-name x)))
      (cdr signature))))
    (signature-syms (append car-signature-syms cdr-signature-syms))
    (signature-string
      (if (< 0 (length signature))
        (format "(~A,)" (string-join (map (lambda (x)
          (format "'~A'" x))
          signature-syms) ", "))
        "( )")))
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


#(define (document-duration obj-pair)
  (let*
    ((name (car obj-pair))
    (value (cdr obj-pair))
    (moment (ly:duration-length value))
    (numerator (ly:moment-main-numerator moment))
    (denominator (ly:moment-main-denominator moment)))
    ; BODY
    (display (format "    '~A': _LilyPondDuration(Duration(~A, ~A), None),\n" name numerator denominator))))


#(define (document-other obj-pair) 
  (let*
    ((name (car obj-pair))
    (value (cdr obj-pair))
    (formatted-value
      (cond
        ((number? value) value)
        ((string? value) (format "'~A'" value))
        (else (format "'~A'" name)))))
    ; BODY
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
    ((ly:duration? (cdr obj-pair))
      (document-duration obj-pair))
  (else 
    (document-other obj-pair))))


#(display "from abjad.tools.durationtools import Duration\n")
#(display "from abjad.tools.lilypondparsertools._LilyPondDuration._LilyPondDuration \\\n")
#(display "    import _LilyPondDuration\n\n\n")
#(display (format "lilypond_version = \"~A\"\n\n" (lilypond-version)))
#(display "current_module = {\n")
#(for-each document-object current-module-sorted)
#(display "}")
