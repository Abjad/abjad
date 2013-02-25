from abjad.tools import markuptools


def make_reference_manual_lilypond_file(music=None):
    r'''.. versionadded:: 2.9

    Make reference manual LilyPond file.

        >>> score = Score([Staff('c d e f')])
        >>> lilypond_file = documentationtools.make_reference_manual_lilypond_file(score)

    ::

        >>> f(lilypond_file) # doctest: +SKIP

        \version "2.15.37"
        \language "english"
        \include "/Users/trevorbaca/Documents/abjad/trunk/abjad/cfg/abjad.scm"

        \layout {
            indent = #0
            ragged-right = ##t
            \context {
                \Score
                \remove Bar_number_engraver
                \override SpacingSpanner #'strict-grace-spacing = ##t
                \override SpacingSpanner #'strict-note-spacing = ##t
                \override SpacingSpanner #'uniform-stretching = ##t
                \override TupletBracket #'bracket-visibility = ##t
                \override TupletBracket #'minimum-length = #3
                \override TupletBracket #'padding = #2
                \override TupletBracket #'springs-and-rods = #ly:spanner::set-spacing-rods
                \override TupletNumber #'text = #tuplet-number::calc-fraction-text
                proportionalNotationDuration = #(ly:make-moment 1 32)
                tupletFullLength = True
            }
        }

        \paper {
            left-margin = 1.0\in
        }

        \score {
            \new Score <<
                \new Staff {
                    c4
                    d4
                    e4
                    f4
                }
            >>
        }

    Return LilyPond file.
    '''
    from abjad.tools import lilypondfiletools
    from abjad.tools import schemetools

    lilypond_file = lilypondfiletools.make_basic_lilypond_file(music=music)

    # header
    lilypond_file.header_block.tagline = markuptools.Markup('""')

    # layout
    lilypond_file.layout_block.indent = 0
    lilypond_file.line_width = lilypondfiletools.LilyPondDimension(6, 'in')
    lilypond_file.layout_block.ragged_right = True

    # paper
    lilypond_file.paper_block.left_margin = lilypondfiletools.LilyPondDimension(1, 'in')

    # score context
    context_block = lilypondfiletools.ContextBlock()
    context_block.context_name = 'Score'
    context_block.engraver_removals.append('Bar_number_engraver')
    context_block.override.spacing_spanner.strict_grace_spacing = True
    context_block.override.spacing_spanner.strict_note_spacing = True
    context_block.override.spacing_spanner.uniform_stretching = True
    context_block.override.tuplet_bracket.bracket_visibility = True
    context_block.override.tuplet_bracket.padding = 2
    context_block.override.tuplet_bracket.springs_and_rods = schemetools.Scheme(
        'ly:spanner::set-spacing-rods')
    context_block.override.tuplet_bracket.minimum_length = 3
    context_block.override.tuplet_number.text = schemetools.Scheme('tuplet-number::calc-fraction-text')
    context_block.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 32))
    context_block.set.tupletFullLength = True
    lilypond_file.layout_block.context_blocks.append(context_block)

    # etc
    lilypond_file.file_initial_system_comments[:] = []
    lilypond_file.global_staff_size = 12

    return lilypond_file
