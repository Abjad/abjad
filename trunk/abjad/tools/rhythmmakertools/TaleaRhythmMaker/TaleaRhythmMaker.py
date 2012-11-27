from abjad.tools.rhythmmakertools.DivisionBurnishedTaleaRhythmMaker import \
    DivisionBurnishedTaleaRhythmMaker


class TaleaRhythmMaker(DivisionBurnishedTaleaRhythmMaker):
    r'''.. versionadded:: 2.8

    Talea rhythm-maker.

    Example 1. Basic usage.

    Configure the rhythm-maker at initialization::

        >>> talea, talea_denominator, prolation_addenda = [-1, 4, -2, 3], 16, [3, 4]
        >>> maker = rhythmmakertools.TaleaRhythmMaker(
        ...     talea, talea_denominator, prolation_addenda)

    Then call the rhythm-maker on arbitrary divisions::

        >>> divisions = [(2, 8), (5, 8)]
        >>> music = maker(divisions)

    The resulting Abjad objects can be included in any score and the rhythm-maker
    can be called indefinitely on other arbitrary sequences of divisions::

        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                \times 4/7 {
                    r16
                    c'4
                    r8
                }
            }
            {
                \time 5/8
                \fraction \times 5/7 {
                    c'8.
                    r16
                    c'4
                    r8
                    c'8.
                    r16
                }
            }
        }

    Example 2. Tie split notes.

        >>> maker = rhythmmakertools.TaleaRhythmMaker([5], 16, tie_split_notes=True)

    Then call the rhythm-maker on arbitrary divisions::

        >>> divisions = [(2, 8), (2, 8), (2, 8), (2, 8)]
        >>> music = maker(divisions)

    The resulting Abjad objects can be included in any score and the rhythm-maker
    can be called indefinitely on other arbitrary sequences of divisions::

        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'4 ~
            }
            {
                c'16
                c'8. ~
            }
            {
                c'8
                c'8 ~
            }
            {
                c'8.
                c'16
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### INITIALIZER ###

    def __init__(self, talea, talea_denominator, prolation_addenda=None, secondary_divisions=None,
        talea_helper=None, prolation_addenda_helper=None, secondary_divisions_helper=None,
        beam_each_cell=False, beam_cells_together=False, tie_split_notes=False):
        lefts, middles, rights = [0], [0], [0]
        left_lengths, right_lengths = [0], [0]
        DivisionBurnishedTaleaRhythmMaker.__init__(self, talea, talea_denominator, prolation_addenda,
            lefts, middles, rights, left_lengths, right_lengths, secondary_divisions,
            talea_helper=talea_helper, prolation_addenda_helper=prolation_addenda_helper,
            secondary_divisions_helper=secondary_divisions_helper,
            beam_each_cell=beam_each_cell, beam_cells_together=beam_cells_together,
            tie_split_notes=tie_split_notes)
