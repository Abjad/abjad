% {score_title} {forces_tagline}
% part_identifier = {part_identifier}

{lilypond_version_directive}
{lilypond_language_directive}

#(ly:set-option 'relative-includes #t)
\include "../stylesheet.ily"
{segment_ily_include_statements}

\paper {{
    evenFooterMarkup =
        \markup
        \on-the-fly #print-page-number-check-first
        \fill-line {{
            " "
            \bold
            \fontsize #3
            \override #'(font-name . "Palatino")
            \line {{
                \override #'(font-name . "Palatino Italic")
                {{ {score_title_without_year} }}
                \hspace #1.5
                —
                \hspace #1.5
                \on-the-fly #print-page-number-check-first
                \fromproperty #'page:page-number-string
                \hspace #1.5
                —
                \hspace #1.5
                \override #'(font-name . "Palatino Italic")
                {{ {forces_tagline} }}
                \hspace #1.5
            }}
            " "
        }}
    oddFooterMarkup = \evenFooterMarkup
}}

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
