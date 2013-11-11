# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import contextualize


def make_text_alignment_example_lilypond_file(music=None):
    r'''Make text-alignment example LilyPond file with `music`.

        >>> score = Score([Staff('c d e f')])
        >>> lilypond_file = documentationtools.make_text_alignment_example_lilypond_file(score)

    ..  doctest::

        >>> print format(lilypond_file) # doctest: +SKIP
        % Abjad revision 5651
        % 2012-05-19 10:04

        \version "2.15.37"
        \language "english"

        #(set-global-staff-size 18)

        \layout {
            indent = #0
            ragged-right = ##t
            \context {
                \Score
                \remove Bar_number_engraver
                \remove Default_bar_line_engraver
                \override Clef #'transparent = ##t
                \override SpacingSpanner #'strict-grace-spacing = ##t
                \override SpacingSpanner #'strict-note-spacing = ##t
                \override SpacingSpanner #'uniform-stretching = ##t
                \override TextScript #'staff-padding = #4
                proportionalNotationDuration = #(ly:make-moment 1 32)
            }
        }

        \paper {
            bottom-margin = #10
            left-margin = #10
            line-width = #150
            system-system-spacing = #'(
                (basic-distance . 0) (minimum-distance . 0) (padding . 15) (stretchability . 0))
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
    from abjad.tools import layouttools
    from abjad.tools import lilypondfiletools
    from abjad.tools import schemetools

    lilypond_file = lilypondfiletools.make_basic_lilypond_file(music=music)

    lilypond_file.global_staff_size = 18

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)

    context_block.engraver_removals.append('Bar_number_engraver')
    context_block.engraver_removals.append('Default_bar_line_engraver')
    context_block.context_name = 'Score'
    override(context_block).clef.transparent = True
    override(context_block).spacing_spanner.strict_grace_spacing = True
    override(context_block).spacing_spanner.strict_note_spacing = True
    override(context_block).spacing_spanner.uniform_stretching = True
    override(context_block).text_script.staff_padding = 4
    override(context_block).time_signature.transparent = True
    contextualize(context_block).proportionalNotationDuration = \
        schemetools.SchemeMoment((1, 32))

    lilypond_file.paper_block.bottom_margin = 10
    lilypond_file.paper_block.left_margin = 10
    lilypond_file.paper_block.line_width = 150

    vector = layouttools.make_spacing_vector(0, 0, 15, 0)
    lilypond_file.paper_block.system_system_spacing = vector

    return lilypond_file
