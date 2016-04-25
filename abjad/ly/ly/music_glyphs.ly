\version "2.19.24"

#(load "helpers.scm")

#(begin

  (define (format-musicglyphs)
    (string-append
      "music_glyphs = "
      (format-string-set
        (format-string-list
          (sort
            (delete ".notdef"
              (ly:otf-glyph-list (ly:system-font-load "emmentaler-20")))
            string<)
          0))
      "\n"))

  ;;; output
  (display
    (string-append
      (format "lilypond_version = \"~A\"\n\n" (lilypond-version))
      (format-musicglyphs)
      )))

% EOF
