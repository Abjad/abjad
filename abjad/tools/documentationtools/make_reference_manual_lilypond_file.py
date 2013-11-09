# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import contextualize


def make_reference_manual_lilypond_file(music=None):
    r'''Make reference manual LilyPond file.

        >>> score = Score([Staff('c d e f')])
        >>> lilypond_file = \
        ...     documentationtools.make_reference_manual_lilypond_file(score)

    ..  doctest::

        >>> f(lilypond_file) # doctest: +SKIP

        \version "2.15.37"
        \language "english"

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

    Returns LilyPond file.
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
    lilypond_file.paper_block.left_margin = \
        lilypondfiletools.LilyPondDimension(1, 'in')

    # score context
    context_block = lilypondfiletools.ContextBlock()
    context_block.context_name = 'Score'
    context_block.engraver_removals.append('Bar_number_engraver')
    override(context_block).spacing_spanner.strict_grace_spacing = True
    override(context_block).spacing_spanner.strict_note_spacing = True
    override(context_block).spacing_spanner.uniform_stretching = True
    override(context_block).tuplet_bracket.bracket_visibility = True
    override(context_block).tuplet_bracket.padding = 2
    override(context_block).tuplet_bracket.springs_and_rods = \
        schemetools.Scheme('ly:spanner::set-spacing-rods')
    override(context_block).tuplet_bracket.minimum_length = 3
    override(context_block).tuplet_number.text = \
        schemetools.Scheme('tuplet-number::calc-fraction-text')
    contextualize(context_block).proportionalNotationDuration = \
        schemetools.SchemeMoment((1, 32))
    contextualize(context_block).tupletFullLength = True
    lilypond_file.layout_block.context_blocks.append(context_block)

    # etc
    lilypond_file.file_initial_system_comments[:] = []
    lilypond_file.global_staff_size = 12

    return lilypond_file
