% Use these functions to make music inside markup functions.
% Note that these are music functions and not markup functions.
% But you can use these music functions within markup functions.


abjad-make-note = #(
    define-music-function
    (parser location length dots)
    (number? number?)
    (make-music
        'SequentialMusic
        'elements
        (list (make-music
                'NoteEvent
                'duration
                (ly:make-duration length dots)
                'pitch
                (ly:make-pitch 0 0))))
    )

abjad-make-tuplet-monad = #(
    define-music-function
    (parser location length dots n d)
    (number? number? number? number?)
    (make-music
        'SequentialMusic
        'elements
        (list (make-music
                'TimeScaledMusic
                'tweaks
                (list (cons (quote edge-height) (cons 0.7 0)))
                'denominator
                d
                'numerator
                n
                'element
                (make-music
                    'SequentialMusic
                    'elements
                    (list (make-music
                            'NoteEvent
                            'duration
                            (ly:make-duration length dots n d)
                            'pitch
                            (ly:make-pitch 0 0)))))))
    )
