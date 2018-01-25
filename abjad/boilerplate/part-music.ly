% {score_title} {forces_tagline}
% part_abbreviation = {part_abbreviation}

{lilypond_version_directive}
{lilypond_language_directive}

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"


\score {{
    <<
        {{
        \include "{dashed_part_name}-layout.ly"
        }}
        {keep_with_tag_command}
        {{
        {segment_include_statements}
        }}
    >>
}}
