from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.rhythmmakertools.BurnishedRhythmMaker import BurnishedRhythmMaker


class OutputBurnishedTaleaRhythmMaker(BurnishedRhythmMaker):
    r'''.. versionadded:: 2.8

    Output-burnished talea rhythm-maker.

    Configure the rhythm-maker at initialization::

        >>> talea, talea_denominator, prolation_addenda = [1, 2, 3], 16, [0, 2]
        >>> lefts, middles, rights = [-1], [0], [-1]
        >>> left_lengths, right_lengths = [1], [1]
        >>> secondary_divisions = [9]
        >>> maker = rhythmmakertools.OutputBurnishedTaleaRhythmMaker(
        ... talea, talea_denominator, prolation_addenda, lefts, middles, rights, 
        ... left_lengths, right_lengths, secondary_divisions)

    Then call the rhythm-maker on arbitrary divisions::

        >>> divisions = [(3, 8), (4, 8)]
        >>> music = maker(divisions)

    The resulting Abjad objects can be included in any score::

        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
        >>> staff = Staff(measures)
        >>> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 3/8
                {
                    r16
                    c'8
                    c'8.
                }
            }
            {
                \time 4/8
                \fraction \times 3/5 {
                    c'16
                    c'8
                    c'8
                }
                {
                    c'16
                    c'16
                    c'8
                    r16
                }
            }
        }

    Usage follows the two-step instantiate-then-call pattern shown here.

    Return rhythm-maker.
    '''

    ### PRIVATE METHODS ###

    def _burnish_division_parts(self, divisions, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        burnished_divisions = []
        left_length = left_lengths[0]
        left = lefts[:left_length]
        right_length = right_lengths[0]
        right = rights[:right_length]
        if len(divisions) == 1:
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            available_right_length = len(divisions[0]) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[0]) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[0], [left_length, middle_length, right_length], cyclic=False, overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = left_part + middle_part + right_part
            burnished_divisions.append(burnished_division)
        else:
            ## first division
            available_left_length = len(divisions[0])
            left_length = min([left_length, available_left_length])
            middle_length = len(divisions[0]) - left_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            left_part, middle_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[0], [left_length, middle_length], cyclic=False, overhang=False)
            left_part = self._burnish_division_part(left_part, left)
            middle_part = self._burnish_division_part(middle_part, middle)
            burnished_division = left_part + middle_part
            burnished_divisions.append(burnished_division)
            ## middle divisions
            for division in divisions[1:-1]:
                middle_part = division
                middle = len(division) * [middles[0]]
                middle_part = self._burnish_division_part(middle_part, middle)
                burnished_division = middle_part
                burnished_divisions.append(burnished_division)
            ## last division:
            available_right_length = len(divisions[-1])
            right_length = min([right_length, available_right_length])
            middle_length = len(divisions[-1]) - right_length
            right = right[:right_length]
            middle = middle_length * [middles[0]]
            middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                divisions[-1], [middle_length, right_length], cyclic=False, overhang=False)
            middle_part = self._burnish_division_part(middle_part, middle)
            right_part = self._burnish_division_part(right_part, right)
            burnished_division = middle_part + right_part
            burnished_divisions.append(burnished_division)
        unburnished_weights = [mathtools.weight(x) for x in divisions]
        burnished_weights = [mathtools.weight(x) for x in burnished_divisions]
        assert burnished_weights == unburnished_weights
        return burnished_divisions
