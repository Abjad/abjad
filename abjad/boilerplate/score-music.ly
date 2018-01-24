% {score_title} {forces_tagline}

{lilypond_version_directive}
{lilypond_language_directive}

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"


\score {{
    <<
        {{
        \include "layout.ly"
        }}
        {{
        {segment_include_statements}
        }}
    >>
}}
