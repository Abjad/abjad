# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import set_


def make_reference_manual_lilypond_file(music=None, **kwargs):
    r'''Makes reference manual LilyPond file.

        >>> score = Score([Staff('c d e f')])
        >>> lilypond_file = \
        ...     documentationtools.make_reference_manual_lilypond_file(score)

    ..  doctest::

        >>> print(format(lilypond_file)) # doctest: +SKIP
        \version "2.19.15"
        \language "english"
        <BLANKLINE>
        #(set-global-staff-size 12)
        <BLANKLINE>
        \header {
            tagline = ##f
        }
        <BLANKLINE>
        \layout {
            indent = #0
            ragged-right = ##t
            \context {
                \Score
                \remove Bar_number_engraver
                \override SpacingSpanner.strict-grace-spacing = ##t
                \override SpacingSpanner.strict-note-spacing = ##t
                \override SpacingSpanner.uniform-stretching = ##t
                \override TupletBracket.bracket-visibility = ##t
                \override TupletBracket.minimum-length = #3
                \override TupletBracket.padding = #2
                \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                \override TupletNumber.text = #tuplet-number::calc-fraction-text
                proportionalNotationDuration = #(ly:make-moment 1 24)
                tupletFullLength = ##t
            }
        }
        <BLANKLINE>
        \paper {
            left-margin = 1\in
        }
        <BLANKLINE>
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

    assert hasattr(music, '__illustrate__')
    lilypond_file = music.__illustrate__(**kwargs)

    blocks = [_ for _ in lilypond_file.items
        if isinstance(_, lilypondfiletools.Block)
        ]
    header_block, layout_block, paper_block = None, None, None
    for block in blocks:
        if block.name == 'header':
            header_block = block
        elif block.name == 'layout':
            layout_block = block
        elif block.name == 'paper':
            paper_block = block

    # paper
    if paper_block is None:
        paper_block = lilypondfiletools.Block(name='paper')
        lilypond_file.items.insert(0, paper_block)
    paper_block.left_margin = lilypondfiletools.LilyPondDimension(1, 'in')

    # layout
    if layout_block is None:
        layout_block = lilypondfiletools.Block(name='layout')
        lilypond_file.items.insert(0, layout_block)
    # TODO: following line does nothing; must assign to paper_block instead
    #lilypond_file.line_width = lilypondfiletools.LilyPondDimension(6, 'in')
    layout_block.indent = 0
    layout_block.ragged_right = True

    # score context
    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Score',
        )
    context_block.remove_commands.append('Bar_number_engraver')
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
    moment = schemetools.SchemeMoment((1, 24))
    set_(context_block).proportionalNotationDuration = moment
    set_(context_block).tupletFullLength = True
    layout_block.items.append(context_block)

    # header
    if header_block is None:
        header_block = lilypondfiletools.Block(name='header')
        lilypond_file.items.insert(0, header_block)
    header_block.tagline = markuptools.Markup('""')

    # etc
    lilypond_file._date_time_token = None
    lilypond_file._global_staff_size = 12

    return lilypond_file
