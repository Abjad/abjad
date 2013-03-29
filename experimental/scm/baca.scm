#(define (funky-time-signature-engraver ctx)
  (let ((time-signature '())
        (last-fraction #f))
    `((process-music
       . ,(lambda (trans)
            (let ((frac (ly:context-property ctx 'timeSignatureFraction)))
              (if (and (null? time-signature)
                       (not (equal? last-fraction frac))
                       (pair? frac))
                  (begin
                    (set! time-signature
                          (ly:engraver-make-grob trans 'TimeSignature '()))
                    (set! (ly:grob-property time-signature 'fraction) frac)

                    (and (not last-fraction)
                         (set! (ly:grob-property time-signature
'break-visibility)
                               (ly:context-property ctx
'implicitTimeSignatureVisibility)))

                    (set! last-fraction frac))))))

      (stop-translation-timestep
       . ,(lambda (trans)
            (set! time-signature '()))))))








#(define (has-interface? grob interface)
 (member interface
        (assoc-get 'interfaces
                   (ly:grob-property grob 'meta))))

#(define (find-system grob)
 (if (has-interface? grob 'system-interface)
    grob
    (find-system (ly:grob-parent grob X))))

#(define (first-musical-column grobl)
 (if (not (eqv? #t (ly:grob-property (car grobl) 'non-musical)))
    (car grobl)
    (first-musical-column (cdr grobl))))

#(define (change-bound grob)
 (let* ((system (find-system grob))
       (cols (ly:grob-array->list (ly:grob-object system 'columns)))
       (musical-column (first-musical-column cols)))
  (ly:spanner-set-bound! grob LEFT musical-column)))

#(define (internal-custom-horizontal-bracket-alignment-callback grob)
 (let* (
        ;; have we been split?
        (orig (ly:grob-original grob))

        ;; if yes, get the split pieces (our siblings)
        (siblings (if (ly:grob? orig)
                      (ly:spanner-broken-into orig)
                      '())))

   (if (and (>= (length siblings) 2)
            (eq? (car (reverse siblings)) grob))
            (and
              (ly:grob-set-property! grob 'connect-to-neighbor (cons #t
#f))
              (change-bound grob))
     )))

#(define (custom-horizontal-bracket-alignment-callback grob)
 (internal-custom-horizontal-bracket-alignment-callback grob)
 (ly:horizontal-bracket::print grob))
