\version "2.16.1"

#(define (format-string-list list indent)
    (cond
        ((null? list) "[]")
        (else 
            (string-append
                "[\n"
                (string-join
                    (map (lambda (s)
                        (string-append
                            (make-string (+ 4 indent) #\space)
                            "\""
                            s
                            "\", \n"))
                        list)
                    "")
                (make-string indent #\space)
                "]"))))

#(define (format-musicglyphs)
    (string-append
        "music_glyphs = "
        (format-string-list
            (sort
                (delete ".notdef"
                    (ly:otf-glyph-list (ly:system-font-load "emmentaler-20")))
                string<)
            0)
        "\n"))

#(display (format "lilypond_version = \"~A\"\n\n" (lilypond-version)))
#(display (format-musicglyphs))
