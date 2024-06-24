\version "2.25.16"

% FROM DAVID NALESNIK:
%
% https://lists.gnu.org/archive/html/lilypond-user/2015-10/msg00545.html
% Implements commands for (up to four) simultaneous text spanners:
%
%    \startTextSpan (LilyPond default)
%    \stopTextSpan (LilyPond default)
%
%    \startTextSpanOne
%    \startTextSpanTwo
%    \startTextSpanThree
%
%    \stopTextSpanOne
%    \stopTextSpanTwo
%    \stopTextSpanThre

%% Incorporating some code from the rewrite in scheme of
%% Text_spanner_engraver in input/regression/scheme-text-spanner.ly

#(define (add-bound-item spanner item)
   (if (null? (ly:spanner-bound spanner LEFT))
       (ly:spanner-set-bound! spanner LEFT item)
       (ly:spanner-set-bound! spanner RIGHT item)))

#(define (axis-offset-symbol axis)
   (if (eq? axis X) 'X-offset 'Y-offset))

#(define (set-axis! grob axis)
   (if (not (number? (ly:grob-property grob 'side-axis)))
       (begin
        (set! (ly:grob-property grob 'side-axis) axis)
        (ly:grob-chain-callback
         grob
         (if (eq? axis X)
             ly:side-position-interface::x-aligned-side
             side-position-interface::y-aligned-side)
         (axis-offset-symbol axis)))))

#(define (assign-spanner-index spanner orig-ls)
   "Determine the position of a new spanner in an ordered sequence
of spanners.  The goal is for the sequence to begin with zero and
contain no gaps.  Return the index representing the spanner's position."
   (if (null? orig-ls)
       0
       (let loop ((ls orig-ls) (insert? #t) (result 0))
         (cond
          ((null? ls) result)
          ;; position at head of list
          ((and insert? (> (caar orig-ls) 0))
           (loop ls #f 0))
          ;; no gaps, put at end of list
          ((and insert? (null? (cdr ls)))
           (loop (cdr ls) #f (1+ (caar ls))))
          ;; fill lowest position of gap
          ((and insert?
                (> (caadr ls) (1+ (caar ls))))
           (loop (cdr ls) #f (1+ (caar ls))))
          (else (loop (cdr ls) insert? result))))))

alternateTextSpannerEngraver =
#(lambda (context)
   (let (;; a list of pairs comprising a spanner index
          ;;  (not spanner-id) and a spanner which has been begun
          (spanners '())
          (finished '()) ; list of spanners in completion stage
          (start-events '()) ; list of START events
          (stop-events '())) ; list of STOP events
     (make-engraver
      ;; \startTextSpan, \stopTextSpan, and the like create events
      ;; which we collect here.
      (listeners
       ((text-span-event engraver event)
        (if (= START (ly:event-property event 'span-direction))
            (set! start-events (cons event start-events))
            (set! stop-events (cons event stop-events)))))
      ;; Populate 'note-columns property of spanners.  Bounds are
      ;; set to note columns, and each spanner keeps a record of
      ;; the note columns it traverses.
      (acknowledgers
       ((note-column-interface engraver grob source-engraver)
        (for-each (lambda (s)
                    (ly:pointer-group-interface::add-grob
                     (cdr s) 'note-columns grob)
                    (add-bound-item (cdr s) grob))
          spanners)
        ;; finished only contains spanners, no indices
        (for-each (lambda (f)
                    (ly:pointer-group-interface::add-grob
                     f 'note-columns grob)
                    (add-bound-item f grob))
          finished)))

      ((process-music trans)
       ;; Move begun spanners from 'spanners' to 'finished'.  We do this
       ;; on the basis of 'spanner-id.  If we find a match--either
       ;; the strings are the same, or both are unset--a transfer
       ;; can be made.  Return a warning if we find no match: spanner
       ;; hasn't been properly begun.
       (for-each
        (lambda (es)
          (let ((es-id (ly:event-property es 'spanner-id)))
            (let loop ((sp spanners))
              (if (null? sp)
                  (ly:warning "No spanner to end!!")
                  (let ((sp-id (ly:event-property
                                (event-cause (cdar sp)) 'spanner-id)))
                    (cond
                     ((or
                       (and
                        (string? sp-id)
                        (string? es-id)
                        (string=? sp-id es-id))
                       ;; deal with \startTextSpan, \stopTextSpan
                       (and
                        (null? sp-id)
                        (null? es-id)))
                      (set! finished (cons (cdar sp) finished))
                      (set! spanners (remove (lambda (s) (eq? s (car sp))) spanners)))
                     (else (loop (cdr sp)))))))))
        stop-events)

       ;; The end of our spanners can be acknowledged by other engravers.
       (for-each
        (lambda (f)
          (ly:engraver-announce-end-grob trans f (event-cause f)))
        finished)

       ;; Make spanners in response to START events.
       ;;
       ;; Each new spanner is assigned an index denoting its position relative to
       ;; other active spanners.  This is enforced (for the moment) by adding
       ;; a small amount to the spanner's 'outside-staff-priority proportional to
       ;; this index.  This is unlikely to result in conflicts, though a better
       ;; solution may be to organize the spanners by a new alignment grob.
       ;;
       ;; Also, add any existing spanners to the 'side-support-elements array of
       ;; the new spanner.  This ensures correct ordering over line breaks when
       ;; 'outside-staff-priority is set to #f (which means that it is no longer
       ;; an outside-staff-object--not the default).
       (for-each
        (lambda (es)
          (let* ((new (ly:engraver-make-grob trans 'TextSpanner es))
                 (new-idx (assign-spanner-index new spanners))
                 (new-osp (ly:grob-property new 'outside-staff-priority))
                 (new-osp (if (number? new-osp)
                              (+ new-osp (/ new-idx 1000.0))
                              new-osp)))
            (set! (ly:grob-property new 'outside-staff-priority) new-osp)
            (set-axis! new Y)
            ;; Add spanners with a lower index than new spanner to
            ;; its 'side-support-elements.  This allows new spanners
            ;; to fill gaps under the topmost spanner.
            (for-each
             (lambda (sp)
               (if (< (car sp) new-idx)
                   (ly:pointer-group-interface::add-grob new
                     'side-support-elements (cdr sp))))
             spanners)
            (set! spanners (cons (cons new-idx new) spanners))
            (set! spanners
                  (sort spanners (lambda (x y) (< (car x) (car y)))))))
        start-events)
       ;; Events have served their purpose for this timestep.  Clear
       ;; the way for new events in later timesteps.
       (set! start-events '())
       (set! stop-events '()))

      ((stop-translation-timestep trans)
       ;; Set bounds of spanners to PaperColumns if they haven't been set.
       ;; This allows spanners to be drawn between spacers.  Other uses?
       ;; Doesn't appear to affect whether spanners can de drawn between
       ;; rests.
       (for-each
        (lambda (s)
          (if (null? (ly:spanner-bound (cdr s) LEFT))
              (ly:spanner-set-bound! (cdr s) LEFT
                (ly:context-property context 'currentMusicalColumn))))
        spanners)

       (for-each
        (lambda (f)
          (if (null? (ly:spanner-bound f RIGHT))
              (ly:spanner-set-bound! f RIGHT
                (ly:context-property context 'currentMusicalColumn))))
        finished)

       (set! finished '()))

      ((finalize trans)
       ;; If spanner ends on spacer at end of context?
       (for-each
        (lambda (f)
          (if (null? (ly:spanner-bound f RIGHT))
              (ly:spanner-set-bound! f RIGHT
                (ly:context-property context 'currentMusicalColumn))))
        finished)
       (set! finished '())
       ;; User didn't end spanner.
       (for-each
        (lambda (sp)
          (ly:warning "incomplete spanner removed!")
          (ly:grob-suicide! (cdr sp)))
        spanners)
       (set! spanners '())))))


startTextSpanOne =
#(make-music 'TextSpanEvent 'span-direction START 'spanner-id "1")

stopTextSpanOne =
#(make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "1")

startTextSpanTwo =
#(make-music 'TextSpanEvent 'span-direction START 'spanner-id "2")

stopTextSpanTwo =
#(make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "2")

startTextSpanThree =
#(make-music 'TextSpanEvent 'span-direction START 'spanner-id "3")

stopTextSpanThree =
#(make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "3")

%%% ENGRAVER SWAP TO MAKE COMMANDS WORK CORRECTLY %%%

\layout {
    \context {
        \Voice
        \remove Text_spanner_engraver
        \consists \alternateTextSpannerEngraver
    }
}
