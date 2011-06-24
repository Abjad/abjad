beam = #(define-music-function (parser location left right) (number? number?)
   #{
      \set stemLeftBeamCount = #$left
      \set stemRightBeamCount = #$right
   #})


fraction = #(define-music-function (parser location music) (ly:music?)
   #{
      \tweak #'text #tuplet-number::calc-fraction-text $music
   #})


white = #(define-music-function (parser location music) (ly:music?)
   #{
      \once \override NoteHead #'duration-log = #1 $music
   #})


transparent = #(define-music-function (parser location music) (ly:music?)
   #{
      \once \override NoteHead #'transparent = ##t
      \once \override NoteHead #'no-ledgers = ##t
      \once \override Stem #'transparent = ##t
      \once \override Dots #'transparent = ##t
      $music
   #})


headless = #(define-music-function (parser location music) (ly:music?)
   #{
      \once \override NoteHead #'transparent = ##t 
      \once \override NoteHead #'no-ledgers = ##t
      $music
   #})


whichContext = #(define-music-function (parser location) ( )
   (make-music 'ApplyContext
               'origin location
               'procedure
      (lambda (c)
         (display
            (string-append
               "\nCurrent voice is "
               (ly:context-id c)
               "\n")))))


locationWhichContext = #(define-music-function (parser location) ( )
   (make-music 'ApplyContext
               'origin location
               'procedure 
      (lambda (c)
         (display
            (ly:input-message location
               "current voice is ~a"
               (ly:context-id c))))))


#(define lastNoteHeadWidth 0)


#(define (centerTextFn grob grob-origin context)    
   '''From Michael Lauer on LilyPond user list.'''
   (cond 
      ((grob::has-interface grob 'note-head-interface)                
         (set! lastNoteHeadWidth (cdr (ly:grob-property grob 'X-extent))))
      ((grob::has-interface grob 'text-script-interface)
           (let* 
               ((xext (ly:grob-property grob 'X-extent))
               (offset (* (- lastNoteHeadWidth (car xext) (cdr xext)) 0.5)))
            (ly:grob-set-property! grob 'X-offset offset)))))


centerText = \applyOutput #'Voice #centerTextFn


%% TODO: Parameterize x-value extra offset or take from global staff size %%
adjustEOLTimeSignatureBarlineExtraOffset = #(define-music-function (parser location) ( )
   #{ 
      #(define (foo grob)
         (if (<= (ly:item-break-dir grob) 0)
            (ly:grob-set-property! grob 'extra-offset (cons 3 0)) '( ) ))
      #(define (bar grob)
         (if (<= (ly:item-break-dir grob) 0)
            (ly:grob-set-property! grob 'extra-offset (cons 3 0)) '( ) ))
      \once \override Score.TimeSignature #'after-line-breaking = #foo
      \once \override Score.BarLine #'after-line-breaking = #bar
      \once \override Score.SpanBar #'after-line-breaking = #bar
   #})


bridgeClefStencil =
    #(ly:make-stencil
        `(path 0.2
            `(rmoveto 0 3.5
            rlineto 0 -7
            rmoveto 0.5 7
            rlineto 0 -7
            rmoveto 0.5 7
            rlineto 0 -7
            rmoveto 0.5 7
            rlineto 0 -7
            rlineto 0.5 4.5
            rlineto -2.5 0
            rlineto 0.5 -4.5
            rmoveto -1 6
            rcurveto 1 0.5 2.5 0.5 3.5 0))
        (cons -1 1)
        (cons -3.5 3.5))
