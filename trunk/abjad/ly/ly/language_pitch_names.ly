\version "2.14.1"

%%% DEFINITIONS %%%

#(define handle-language (lambda (x) (begin
    (print-language x)
    (display " {")
    (map print-pitch (cdr x))
    (display "\n    },\n"))))

#(define print-language (lambda (x) (display
    (format "~%    '~A':" (car x)))))

#(define print-pitch (lambda (x) (display 
    (format "~%        '~A': ~A,"
        (car x)
        (* 0.5 (+ 24 (ly:pitch-quartertones (cdr x))))))))

%%% MAIN %%%

#(begin
    (display "language_pitch_names = {")
    (map handle-language language-pitch-names)
    (display "\n}"))
