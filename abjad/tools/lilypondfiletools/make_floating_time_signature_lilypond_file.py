# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import schemetools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_


def make_floating_time_signature_lilypond_file(music=None):
    r'''Makes floating time signature LilyPond file.

    ..  container:: example

        ::

            >>> score = Score()
            >>> time_signature_context = scoretools.Context(
            ...     context_name='TimeSignatureContext',
            ...     )
            >>> durations = [(2, 8), (3, 8), (4, 8)]
            >>> measures = scoretools.make_spacer_skip_measures(durations)
            >>> time_signature_context.extend(measures)
            >>> score.append(time_signature_context)
            >>> staff = Staff()
            >>> staff.append(Measure((2, 8), "c'8 ( d'8 )"))
            >>> staff.append(Measure((3, 8), "e'8 ( f'8  g'8 )"))
            >>> staff.append(Measure((4, 8), "fs'4 ( e'8 d'8 )"))
            >>> score.append(staff)
            >>> lilypond_file = \
            ...     lilypondfiletools.make_floating_time_signature_lilypond_file(
            ...     score
            ...     )

        ::

            >>> print(format(lilypond_file)) # doctest: +SKIP
            % 2014-01-07 18:22

            \version "2.19.0"
            \language "english"

            #(set-default-paper-size "letter" 'portrait)
            #(set-global-staff-size 12)

            \header {}

            \layout {
                \accidentalStyle forget
                indent = #0
                ragged-right = ##t
                \context {
                    \name TimeSignatureContext
                    \type Engraver_group
                    \consists Axis_group_engraver
                    \consists Time_signature_engraver
                    \override TimeSignature.X-extent = #'(0 . 0)
                    \override TimeSignature.X-offset = #ly:self-alignment-interface::x-aligned-on-self
                    \override TimeSignature.Y-extent = #'(0 . 0)
                    \override TimeSignature.break-align-symbol = ##f
                    \override TimeSignature.break-visibility = #end-of-line-invisible
                    \override TimeSignature.font-size = #1
                    \override TimeSignature.self-alignment-X = #center
                    \override VerticalAxisGroup.default-staff-staff-spacing = #'((basic-distance . 0) (minimum-distance . 12) (padding . 6) (stretchability . 0))
                }
                \context {
                    \Score
                    \remove Bar_number_engraver
                    \accepts TimeSignatureContext
                    \override Beam.breakable = ##t
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override TupletBracket.bracket-visibility = ##t
                    \override TupletBracket.minimum-length = #3
                    \override TupletBracket.padding = #2
                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                    autoBeaming = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 32)
                    tupletFullLength = ##t
                }
                \context {
                    \StaffGroup
                }
                \context {
                    \Staff
                    \remove Time_signature_engraver
                }
                \context {
                    \RhythmicStaff
                    \remove Time_signature_engraver
                }
            }

            \paper {
                left-margin = #20
                system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))
            }

            \score {
                \new Score <<
                    \new TimeSignatureContext {
                        {
                            \time 2/8
                            s1 * 1/4
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                    }
                    \new Staff {
                        {
                            \time 2/8
                            c'8 (
                            d'8 )
                        }
                        {
                            \time 3/8
                            e'8 (
                            f'8
                            g'8 )
                        }
                        {
                            \time 4/8
                            fs'4 (
                            e'8
                            d'8 )
                        }
                    }
                >>
            }

        ::

            >>> show(lilypond_file) # doctest: +SKIP

    Makes LilyPond file.

    Wraps `music` in LilyPond ``\score`` block.

    Adds LilyPond ``\header``, ``\layout``, ``\paper`` and ``\score`` blocks to
    LilyPond file.

    Defines layout settings for custom ``\TimeSignatureContext``.

    (Note that you must create and populate an Abjad context with name
    equal to ``'TimeSignatureContext'`` in order for ``\TimeSignatureContext``
    layout settings to apply.)

    Applies many file, layout and paper settings.

    Returns LilyPond file.
    '''
    from abjad.tools import lilypondfiletools

    lilypond_file = lilypondfiletools.make_basic_lilypond_file(
        music=music,
        default_paper_size=('letter', 'portrait'),
        global_staff_size=12,
        )

    lilypond_file.paper_block.left_margin = 20
    vector = schemetools.make_spacing_vector(0, 0, 12, 0)
    lilypond_file.paper_block.system_system_spacing = vector

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    command = indicatortools.LilyPondCommand('accidentalStyle forget')
    lilypond_file.layout_block.items.append(command)

    block = _make_time_signature_context_block(font_size=1, padding=6)
    lilypond_file.layout_block.items.append(block)

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.accepts_commands.append('TimeSignatureContext')
    context_block.remove_commands.append('Bar_number_engraver')
    override(context_block).beam.breakable = True
    override(context_block).spacing_spanner.strict_grace_spacing = True
    override(context_block).spacing_spanner.strict_note_spacing = True
    override(context_block).spacing_spanner.uniform_stretching = True
    override(context_block).tuplet_bracket.bracket_visibility = True
    override(context_block).tuplet_bracket.padding = 2
    scheme = schemetools.Scheme('ly:spanner::set-spacing-rods')
    override(context_block).tuplet_bracket.springs_and_rods = scheme
    override(context_block).tuplet_bracket.minimum_length = 3
    scheme = schemetools.Scheme('tuplet-number::calc-fraction-text')
    override(context_block).tuplet_number.text = scheme
    set_(context_block).autoBeaming = False
    moment = schemetools.SchemeMoment((1, 24))
    set_(context_block).proportionalNotationDuration = moment
    set_(context_block).tupletFullLength = True

    # provided as a stub position for user customization
    context_block = lilypondfiletools.ContextBlock(
        source_context_name='StaffGroup',
        )
    lilypond_file.layout_block.items.append(context_block)

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Staff',
        )

    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Time_signature_engraver')

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='RhythmicStaff',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Time_signature_engraver')

    return lilypond_file


def _make_time_signature_context_block(
    font_size=3,
    minimum_distance=10,
    padding=4,
    ):
    from abjad.tools import lilypondfiletools
    assert isinstance(font_size, (int, float))
    assert isinstance(padding, (int, float))
    context_block = lilypondfiletools.ContextBlock(
        type_='Engraver_group',
        name='TimeSignatureContext',
        )
    context_block.consists_commands.append('Axis_group_engraver')
    context_block.consists_commands.append('Time_signature_engraver')
    override(context_block).time_signature.X_extent = (0, 0)
    override(context_block).time_signature.X_offset = schemetools.Scheme(
        'ly:self-alignment-interface::x-aligned-on-self')
    override(context_block).time_signature.Y_extent = (0, 0)
    override(context_block).time_signature.break_align_symbol = False
    override(context_block).time_signature.break_visibility = \
        schemetools.Scheme('end-of-line-invisible')
    override(context_block).time_signature.font_size = font_size
    override(context_block).time_signature.self_alignment_X = \
        schemetools.Scheme('center')
    spacing_vector = schemetools.make_spacing_vector(
        0,
        minimum_distance,
        padding,
        0,
        )
    override(context_block).vertical_axis_group.default_staff_staff_spacing = \
        spacing_vector
    return context_block