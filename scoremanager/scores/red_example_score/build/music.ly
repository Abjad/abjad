% Red Example Score (2013) for piano

\version "2.17.27"
\language "english"
\include "/Users/trevorbaca/Documents/abjad/scoremanager/scores/red_example_score/stylesheets/stylesheet.ily"

\context Score = "Red Example Score" {
    \include "/Users/trevorbaca/Documents/abjad/scoremanager/scores/red_example_score/build/segment-01.ly"
    \include "/Users/trevorbaca/Documents/abjad/scoremanager/scores/red_example_score/build/segment-02.ly"
    \include "/Users/trevorbaca/Documents/abjad/scoremanager/scores/red_example_score/build/segment-03.ly"
}