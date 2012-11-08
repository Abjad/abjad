from abjad.tools.rhythmmakertools.DivisionBurnishedTaleaFilledRhythmMaker import \
    DivisionBurnishedTaleaFilledRhythmMaker


class TaleaFilledRhythmMaker(DivisionBurnishedTaleaFilledRhythmMaker):
    r'''.. versionadded:: 2.8

    Talea-filled rhythm-maker.

    Configure the rhythm-maker at initialization::

        >>> talea, denominator, prolation_addenda = [-1, 4, -2, 3], 16, [3, 4]
        >>> maker = rhythmmakertools.TaleaFilledRhythmMaker(
        ...     talea, denominator, prolation_addenda)

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

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### INITIALIZER ###

    def __init__(self, talea, denominator, prolation_addenda=None, secondary_divisions=None,
        talea_helper=None, prolation_addenda_helper=None, secondary_divisions_helper=None,
        beam_each_cell=False):
        lefts, middles, rights = [0], [0], [0]
        left_lengths, right_lengths = [0], [0]
        DivisionBurnishedTaleaFilledRhythmMaker.__init__(self, talea, denominator, prolation_addenda,
            lefts, middles, rights, left_lengths, right_lengths, secondary_divisions,
            talea_helper=talea_helper, prolation_addenda_helper=prolation_addenda_helper,
            secondary_divisions_helper=secondary_divisions_helper,
            beam_each_cell=beam_each_cell)
