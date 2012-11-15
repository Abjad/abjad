from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.BurnishedRhythmMaker import BurnishedRhythmMaker


class DivisionBurnishedTaleaRhythmMaker(BurnishedRhythmMaker):
    r'''.. versionadded:: 2.8

    Division-burnished talea-filled rhythm-maker.

    Configure the rhythm-maker at instantiation::

        >>> talea, talea_denominator, prolation_addenda = [1, 1, 2, 4], 32, [0, 3]
        >>> lefts, middles, rights = [-1], [0], [-1]
        >>> left_lengths, right_lengths = [1], [1]
        >>> secondary_divisions = [14]
        >>> maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        ... talea, talea_denominator, prolation_addenda, lefts, middles, rights, 
        ... left_lengths, right_lengths, secondary_divisions)

    Then call the rhythm-maker on any sequence of divisions::

        >>> divisions = [(5, 16), (6, 16)]
        >>> music = maker(divisions)

    The resulting Abjad objects can then be included in any score and the rhythm
    maker can be called again and again on different divisions::

        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 5/16
                {
                    r32
                    c'32
                    c'16
                    c'8
                    c'32
                    r32
                }
            }
            {
                \time 6/16
                \times 4/7 {
                    r16
                    c'8
                    r32
                }
                {
                    r32
                    c'16
                    c'8
                    r32
                }
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### PRIVATE METHODS ###

    def _burnish_division_parts(self, divisions, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths=quintuplet
        lefts_index, rights_index = 0, 0
        burnished_divisions = []
        for division_index, division in enumerate(divisions):
            left_length = left_lengths[division_index]
            left = lefts[lefts_index:lefts_index+left_length]
            lefts_index += left_length
            right_length = right_lengths[division_index]
            right = rights[rights_index:rights_index+right_length]
            rights_index += right_length
            available_left_length = len(division)
            left_length = min([left_length, available_left_length])
            available_right_length = len(division) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(division) - left_length - right_length

            left = left[:left_length]
            middle = middle_length * [middles[division_index]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                division, [left_length, middle_length, right_length], cyclic=False, overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions
