from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import setting


def make_text_alignment_example_lilypond_file(music=None):
    r'''Makes text-alignment example LilyPond file.

    ..  container:: example

        ::

            >>> score = abjad.Score([abjad.Staff('c d e f')])
            >>> lilypond_file = abjad.documentationtools.make_text_alignment_example_lilypond_file(score)

        ..  docs::

            >>> print(format(lilypond_file)) # doctest: +SKIP
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
                    \override Clef.transparent = ##t
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override TextScript.staff-padding = #4
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
    import abjad
    lilypond_file = abjad.LilyPondFile.new(
        music=music,
        global_staff_size=18,
        )
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    context_block = abjad.ContextBlock(
        source_context_name='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Bar_number_engraver')
    context_block.remove_commands.append('Default_bar_line_engraver')
    override(context_block).clef.transparent = True
    override(context_block).spacing_spanner.strict_grace_spacing = True
    override(context_block).spacing_spanner.strict_note_spacing = True
    override(context_block).spacing_spanner.uniform_stretching = True
    override(context_block).text_script.staff_padding = 4
    override(context_block).time_signature.transparent = True
    moment = abjad.SchemeMoment((1, 32))
    setting(context_block).proportionalNotationDuration = moment
    lilypond_file.paper_block.bottom_margin = 10
    lilypond_file.paper_block.left_margin = 10
    lilypond_file.paper_block.line_width = 150
    vector = abjad.SpacingVector(0, 0, 15, 0)
    lilypond_file.paper_block.system_system_spacing = vector
    return lilypond_file
