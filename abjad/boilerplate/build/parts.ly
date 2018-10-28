\version "{lilypond_version}"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "../../stylesheets/stylesheet.ily"
\include "stylesheet.ily"

#(set-default-paper-size "{paper_size}" '{orientation})
#(set-global-staff-size {global_staff_size})
 
\include "../parts.ily"
