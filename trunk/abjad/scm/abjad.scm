ppppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "pppp" #:hspace 0)))
pppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "ppp" #:hspace 0)))
ppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "pp" #:hspace 0)))
pX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "p" #:hspace 0)))
mpX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "mp" #:hspace 0)))

mX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "m" #:hspace 0)))

mfX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "mf" #:hspace 0)))
fX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "f" #:hspace 0)))
ffX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "ff" #:hspace 0)))
fffX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "fff" #:hspace 0)))
ffffX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "ffff" #:hspace 0)))

sfX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sf" #:hspace 0)))
sffX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sff" #:hspace 0)))
sfffX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfff" #:hspace 0)))

sfzX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfz" #:hspace 0)))
sffzX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sffz" #:hspace 0)))
sfffzX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfffz" #:hspace 0)))

sfpX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfp" #:hspace 0)))
sfppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfpp" #:hspace 0)))
sfpppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfppp" #:hspace 0)))

sffpX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sffp" #:hspace 0)))
sffppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sffpp" #:hspace 0)))
sffpppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sffppp" #:hspace 0)))

sfffpX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfffp" #:hspace 0)))
sfffppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfffpp" #:hspace 0)))
sfffpppX = #(make-dynamic-script (markup #:combine 
   #:transparent #:dynamic "f" 
   #:line(#:hspace 0 #:dynamic "sfffppp" #:hspace 0)))

beam = #(define-music-function (parser location left right) (number? number?)
      #{
         \set stemLeftBeamCount = #$left
         \set stemRightBeamCount = #$right
      #})

fraction = #(define-music-function (parser location music) (ly:music?)
	#{ \tweak #'text #tuplet-number::calc-fraction-text $music #})

triangle = #(define-music-function (parser location music) (ly:music?)
	#{ \once \set shapeNoteStyles = ##(do do do do do do do) $music #})

semicircle = #(define-music-function (parser location music) (ly:music?)
	#{ \once \set shapeNoteStyles = ##(re re re re re re re) $music #})

blackdiamond = #(define-music-function (parser location music) (ly:music?)
	#{ \once \override NoteHead #'style = #'harmonic-black
      $music #})

tiltedtriangle = #(define-music-function (parser location music) (ly:music?)
	#{ \once \set shapeNoteStyles = ##(fa fa fa fa fa fa fa) $music #})

square = #(define-music-function (parser location music) (ly:music?)
	#{ \once \set shapeNoteStyles = ##(la la la la la la la) $music #})

wedge = #(define-music-function (parser location music) (ly:music?)
	#{ \once \set shapeNoteStyles = ##(ti ti ti ti ti ti ti) $music #})

diamond = #(define-music-function (parser location music) (ly:music?)
	#{ \once \override NoteHead #'style = #'harmonic $music #})

% TODO: remove me after compliling SNOW
harmonic = #(define-music-function (parser location music) (ly:music?)
	#{ \once \override NoteHead #'style = #'harmonic $music #})

cross = #(define-music-function (parser location music) (ly:music?)
	#{ \once \set shapeNoteStyles = ##(cross cross cross cross cross cross cross) $music #})

white = #(define-music-function (parser location music) (ly:music?)
	#{ \once \override NoteHead #'duration-log = #1 $music #})

transparent = #(define-music-function (parser location music) (ly:music?)
	#{ \once \override NoteHead #'transparent = ##t 
      \once \override NoteHead #'no-ledgers = ##t
      \once \override Stem #'transparent = ##t
      \once \override Dots #'transparent = ##t
      $music #})

headless = #(define-music-function (parser location music) (ly:music?)
	#{ \once \override NoteHead #'transparent = ##t 
      \once \override NoteHead #'no-ledgers = ##t
      $music #})

whichContext = #(define-music-function (parser location) ()
                (make-music 'ApplyContext
                 'origin location
                 'procedure (
                   lambda (c)
                   (display
                    (string-append
                     "\nCurrent voice is "
                     (ly:context-id c)
                     "\n")))))

locationWhichContext = #(define-music-function (parser location) ()
                (make-music 'ApplyContext
                 'origin location
                 'procedure (
                   lambda (c)
                   (display
                    (ly:input-message location
                     "current voice is ~a"
                     (ly:context-id c))))))
