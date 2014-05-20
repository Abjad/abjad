% Red Example Score (2013) for piano 

\version "2.19.5"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "../stylesheets/stylesheet.ily"

\context Score = "Red Example Score" {
   \include "segment-01.ly"
   \include "segment-02.ly"
   \include "segment-03.ly"
}