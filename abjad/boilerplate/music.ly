% {score_title} {forces_tagline}

{lilypond_version_directive}
{lilypond_language_directive}

#(ly:set-option 'relative-includes #t)
{stylesheet_include_statement}

\score {{
    {{
    {segment_include_statements}
    }}
}}