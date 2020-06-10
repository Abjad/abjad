% {score_title} {forces_tagline}

{lilypond_version_directive}
{lilypond_language_directive}

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"
{segment_ily_include_statements}


\score {{
    <<
        {{
        \include "layout.ly"
        }}
        {{
        {segment_ly_include_statements}
        }}
    >>
}}
