% {score_title} {forces_tagline}
% part_abbreviation = {part_abbreviation}

{lilypond_version_directive}
{lilypond_language_directive}

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"
{segment_ily_include_statements}

\header {{
    subtitle =
        \markup \column \center-align
        {{
            \override #'(font-name . "Palatino Italic") \fontsize #3
            {{
                \line {{ {part_subtitle} }}
                \line {{ part }}
            }}
        }}
}}


\score {{
    <<
        {{
        \include "{dashed_part_name}-layout.ly"
        }}
        {{
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {{
                    {global_skip_identifiers}
                    }}
                >> 
                \context MusicContext = "MusicContext"
                {{
                    \context Staff = "Staff"
                    {{
                    {segment_ly_include_statements}
                    }}
                }}
            >>
        }}
    >>
}}
