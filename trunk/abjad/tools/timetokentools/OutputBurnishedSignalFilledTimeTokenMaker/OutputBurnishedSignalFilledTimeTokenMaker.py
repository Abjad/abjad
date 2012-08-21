from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.timetokentools.BurnishedTimeTokenMaker import BurnishedTimeTokenMaker


class OutputBurnishedSignalFilledTimeTokenMaker(BurnishedTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Output-burnished signal-filled time-token maker.

    Configure the time-token maker at initialization::

        >>> from abjad.tools import sequencetools
        >>> from abjad.tools import timetokentools

    ::

        >>> pattern, denominator, prolation_addenda = [1, 2, 3], 16, [0, 2]
        >>> lefts, middles, rights = [-1], [0], [-1]
        >>> left_lengths, right_lengths = [1], [1]
        >>> secondary_divisions = [9]
        >>> maker = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
        ... pattern, denominator, prolation_addenda, lefts, middles, rights, 
        ... left_lengths, right_lengths, secondary_divisions)

    Then call the time-token maker on arbitrary duration tokens::

        >>> duration_tokens = [(3, 8), (4, 8)]
        >>> music = maker(duration_tokens)

    The resulting Abjad objects can be included in any score::

        >>> music = sequencetools.flatten_sequence(music)
        >>> measures = measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens)
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

    Return time-token maker.
    '''

    ### PRIVATE METHODS ###

    def _force_token_parts(self, tokens, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths = quintuplet
        forced_tokens = []
        left_length = left_lengths[0]
        left = lefts[:left_length]
        right_length = right_lengths[0]
        right = rights[:right_length]
        if len(tokens) == 1:
            available_left_length = len(tokens[0])
            left_length = min([left_length, available_left_length])
            available_right_length = len(tokens[0]) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(tokens[0]) - left_length - right_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                tokens[0], [left_length, middle_length, right_length], cyclic=False, overhang=False)
            left_part = self._force_token_part(left_part, left)
            middle_part = self._force_token_part(middle_part, middle)
            right_part = self._force_token_part(right_part, right)
            forced_token = left_part + middle_part + right_part
            forced_tokens.append(forced_token)
        else:
            ## first token
            available_left_length = len(tokens[0])
            left_length = min([left_length, available_left_length])
            middle_length = len(tokens[0]) - left_length
            left = left[:left_length]
            middle = middle_length * [middles[0]]
            left_part, middle_part = \
                sequencetools.partition_sequence_by_counts(
                tokens[0], [left_length, middle_length], cyclic=False, overhang=False)
            left_part = self._force_token_part(left_part, left)
            middle_part = self._force_token_part(middle_part, middle)
            forced_token = left_part + middle_part
            forced_tokens.append(forced_token)
            ## middle tokens
            for token in tokens[1:-1]:
                middle_part = token
                middle = len(token) * [middles[0]]
                middle_part = self._force_token_part(middle_part, middle)
                forced_token = middle_part
                forced_tokens.append(forced_token)
            ## last token:
            available_right_length = len(tokens[-1])
            right_length = min([right_length, available_right_length])
            middle_length = len(tokens[-1]) - right_length
            right = right[:right_length]
            middle = middle_length * [middles[0]]
            middle_part, right_part = \
                sequencetools.partition_sequence_by_counts(
                tokens[-1], [middle_length, right_length], cyclic=False, overhang=False)
            middle_part = self._force_token_part(middle_part, middle)
            right_part = self._force_token_part(right_part, right)
            forced_token = middle_part + right_part
            forced_tokens.append(forced_token)
        unforced_weights = [mathtools.weight(x) for x in tokens]
        forced_weights = [mathtools.weight(x) for x in forced_tokens]
        assert forced_weights == unforced_weights
        return forced_tokens
