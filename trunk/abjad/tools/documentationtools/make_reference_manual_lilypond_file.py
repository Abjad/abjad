def make_reference_manual_lilypond_file(music=None):
    r'''.. versionadded:: 2.9

    Make reference manual LilyPond file.

        >>> from abjad.tools import documentationtools

    ::

        >>> score = Score([Staff('c d e f')])
        >>> lilypond_file = documentationtools.make_reference_manual_lilypond_file(score)

    ::

        >>> f(lilypond_file) # doctest: +SKIP
        % Abjad revision 5653
        % 2012-05-19 11:21

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

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)

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

    return lilypond_file
