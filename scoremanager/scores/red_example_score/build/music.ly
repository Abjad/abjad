% Red Example Score (2013) for piano 

\version "2.19.15"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "../stylesheets/stylesheet.ily"

\score {
    {
   \include "segment-01.ly"
   \include "segment-02.ly"
   \include "segment-03.ly"
    }
}