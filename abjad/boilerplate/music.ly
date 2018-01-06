% {score_title} {forces_tagline}

{lilypond_version_directive}
{lilypond_language_directive}

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"


\score {{
    <<
        {keep_with_tag_command}{{
        \include "layout.ly"
        }}
        {keep_with_tag_command}{{
        {segment_include_statements}
        }}
    >>
}}
