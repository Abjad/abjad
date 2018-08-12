% AUTHOR: MIKE SOLOMON

\version "2.19"

%{
  'height of any piece of a broken hairpin is always the same.  It
  represents the rise of either wing of the hairpin.
  
  The stencil Y-extent of the hairpin =
  (-y . y)
  where y =
  
    for full-size pieces:
  height + (0.5 * line-thickness)
  
    for reduced-size pieces:
  (2/3 * height) + (0.5 * line-thickness)
  
  Use the stencil X-extent for X of hairpin.
  
  For Y, it seems more straightforward to use 'height instead of Y-extent,
  because then we can simply draw the wing without needing to factor in
  line-thickness:
  
  height * factor  [either 1.0 or 2/3]
  
%}

#(define-public ((elbowed-hairpin coords x-op mirrored?) grob)
   "Create hairpin based on a list of @var{coords} in @code{(cons x y)}
form.  @code{x} is the portion of the width consumed for a given line
and @code{y} is the portion of the height.  For example,
@code{'((0.3 . 0.7) (0.8 . 0.9) (1.0 . 1.0))} means that at the point
where the hairpin has consumed 30% of its width, it must
be at 70% of its height.  Once it is to 80% width, it
must be at 90% height.  It finishes at
100% width and 100% height.  @var{mirrored?} indicates if the hairpin
is mirrored over the Y-axis or if just the upper part is drawn.
Returns a function that accepts a hairpin grob as an argument
and draws the stencil based on its coordinates.
@lilypond[verbatim,quote]
#(define simple-hairpin
  (elbowed-hairpin '((1.0 . 1.0)) #t))

\\relative c' {
  \\override Hairpin #'stencil = #simple-hairpin
  a\\p\\< a a a\\f
}
@end lilypond
Broken elbowed hairpins are possible, though more complex definitions
(exceeding two pairs for @var{coords}) are not accomodated.
"
   (define (pair-to-list pair)
     (list (car pair) (cdr pair)))
   (define (normalize-coords goods x y)
     (map
      (lambda (coord)
        (cons (x-op x (car coord)) (* y (cdr coord))))
      goods))
   (define (my-c-p-s points thick decresc?)
     (make-connected-path-stencil
      points
      thick
      (if decresc? -1.0 1.0)
      1.0
      #f
      #f))
   ;; outer let to trigger suicide
   (let ((sten (ly:hairpin::print grob)))
     (if (grob::is-live? grob)
         (let* ((orig (ly:grob-original grob))
                (siblings (ly:spanner-broken-into orig))
                (broken? (pair? siblings))
                (first? (or (not broken?)
                            (eq? grob (first siblings))))
                (last? (or (not broken?)
                           (eq? grob (last siblings))))
                (middle? (not (or first? last?)))
                (decresc? (eq? (ly:grob-property grob 'grow-direction) LEFT))
                (cresc? (not decresc?))
                (niente? (ly:grob-property grob 'circled-tip #f))
                ; In the case of a broken hairpin, only one piece will
                ; be `flared' or receive a circle
                (flared? (or (and decresc? first?)
                             (and cresc? last?)))
                (circled? (and niente?
                               (or (and decresc? last?)
                                   (and cresc? first?))))
                (height (ly:grob-property grob 'height 0.2))
                (height (* height (ly:staff-symbol-staff-space grob)))
                ; calculation of radius of circle for circled tip
                ; by method used in `cc/hairpin.cc'
                (rad (* height 0.525))  
                (xex (ly:stencil-extent sten X))
                ; X-extent adjusted for circle at beginning or end
                ; of hairpin
                (xex (if circled?
                         (if decresc?
                             (cons (car xex) (- (cdr xex) (* rad 2)))
                             (cons (+ (car xex) (* rad 2)) (cdr xex)))
                         xex))
                (lenx (interval-length xex))
                (xtrans (+ (car xex) (if decresc? lenx 0)))
                (ytrans (car (ly:stencil-extent sten Y)))
                (thick (ly:grob-property grob 'thickness 0.1))
                (thick (* thick (layout-line-thickness grob)))
                (circle (if circled?
                            (make-circle-stencil rad thick #f)
                            empty-stencil))
                (circle-yex (ly:stencil-extent circle Y))
                ; It is conceptually problematic to draw constante hairpins with the
                ; same routine as flared hairpins.  They are neither crescendos nor
                ; decrescendos, and the 'uptick' does not represent a change in
                ; dynamic level.  Provision is made here to accommodate them, but they
                ; should probably be handled separately, with another grob.
                (constante? (eq? constante-hairpin
                                 (ly:assoc-get 'stencil (ly:grob-basic-properties grob))))
               
                ; The following variables are needed to accommodate differences
                ; in the starting and ending heights of the segments of broken hairpins.
                ; See the definition of ly:hairpin::print in hairpin.cc.
                (small (/ 1 3))
                (mid (/ 2 3))
                (full 1.0)
                (starth
                 (cond
                  ; A constante 'hairpin' only makes sense with the
                  ; 'uptick' at the end, as it simply marks the end of
                  ; the previously indicated dynamic level.  Therefore, we
                  ; produce the same results whether user creates it with
                  ; a cresc. or decresc.
                  (constante? 0.0)
                  ;(if decresc?
                  ;   (if first? full 0.0)
                  ;  0.0))
                  (decresc?
                   (if first? full mid))
                  (cresc?
                   (if first? 0.0 small))))
                (endh
                 (cond
                  (constante?
                   (if last? full 0.0))
                  ;(if decresc?
                  ;   (if last? 0.0 full)
                  ;  full))
                  (decresc?
                   (if last? 0.0 small))
                  (cresc?
                   (if last? full mid))))
                ; Y scale factor for broken and unbroken segments          
                (height-multiplier
                 (abs (- endh starth)))
               
                ; Since make-connected-path-stencil draws from an origin of
                ; (0, 0), segments that don't converge must be translated vertically.
                (offset (if constante?
                            0.0
                            (if decresc?
                                (* endh height)
                                (* starth height))))
                ; If piece is flared, we use the provided coordinates; otherwise,
                ; we draw an ordinary hairpin or horizontal line (constante).  This
                ; means that only the simplest custom hairpins are accomodated.
                (coords (if flared?
                            coords
                            (if constante?
                                ; -->horizontal line
                                (list (cons 1.0 0.0))
                                ; -->ordinary hairpin
                                (list (cons 1.0 1.0)))))
                ; slight adjustment for the unlikely case of a niente constante hairpin
                (ytrans (if (and constante? circled?)
                            (+ ytrans (car circle-yex))
                            ytrans))
                ; scale for broken/unbroken
                (coords (normalize-coords coords 1 height-multiplier))           
                (uplist (map pair-to-list
                          (normalize-coords coords
                            lenx
                            height)))
                (downlist (map pair-to-list
                            (normalize-coords coords
                              lenx
                              (- height))))
                (upstil (my-c-p-s uplist thick decresc?))
                (downstil (if mirrored?
                              (my-c-p-s downlist thick decresc?)
                              empty-stencil)))
           ; The outer stencil-translate produces no effect on the vertical positioning
           ; of the hairpin.
           ;(display ytrans) (newline)
           ;(display offset) (newline)
           (ly:stencil-translate
            (ly:stencil-add
             (ly:stencil-translate
              circle
              (if decresc? (cons rad offset) (cons (- rad) offset)))
             (ly:stencil-translate upstil (cons 0 offset))
             (ly:stencil-translate downstil (cons 0 (- offset))))
            (cons xtrans ytrans))
        
           (ly:stencil-add
            ; ly:stencil-translate can only displace a stencil vertically
            ; with relation to another stencil.
            point-stencil
            (ly:stencil-translate
             (ly:stencil-add
              (ly:stencil-translate
               circle
               (if decresc? (cons rad offset) (cons (- rad) offset)))
              (ly:stencil-translate upstil (cons 0 offset))
              (ly:stencil-translate downstil (cons 0 (- offset))))
             (cons xtrans ytrans))))
         '())))

% NOTE: changed from Mike Solomon's original definition:
#(define-public abjad-flared-hairpin
  (elbowed-hairpin '((1.0 . 0.4) (1.25 . 1.0)) - #t))

#(define-public constante-hairpin
   (elbowed-hairpin '((1.0 . 0.0) (1.0 . 1.0)) * #f))

%#(define-public normal-hairpin
%   (elbowed-hairpin '((1.0 . 1.0)) * #t))
%
%#(define-public bizarre-hairpin
%   (elbowed-hairpin '((0.5 . 1.0) (0.6 . 0.2) (0.8 . 1.2) (0.9 . 0.0) (1.0 . 1.0)) * #t))
