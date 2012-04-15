from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.timetokentools.BurnishedTimeTokenMaker import BurnishedTimeTokenMaker


class TokenBurnishedSignalFilledTimeTokenMaker(BurnishedTimeTokenMaker):
    r'''.. versionadded:: 2.8

    Token-burnished signal-filled time-token maker.

    Configure the time-token maker at instantiation::

        abjad> from abjad.tools import sequencetools
        abjad> from abjad.tools import timetokentools

    ::

        abjad> pattern, denominator, prolation_addenda = [1, 1, 2, 4], 32, [0, 3]
        abjad> lefts, middles, rights = [-1], [0], [-1]
        abjad> left_lengths, right_lengths = [1], [1]
        abjad> secondary_divisions = [14]
        abjad> maker = timetokentools.TokenBurnishedSignalFilledTimeTokenMaker(pattern, denominator, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths, secondary_divisions)

    Then call the time-token maker on any sequence of duration tokens::

        abjad> duration_tokens = [(5, 16), (6, 16)]
        abjad> music = maker(duration_tokens)

    The resulting Abjad objects can then be included in any score and the time-token
    maker can be called again and again on different duration tokens::

        abjad> music = sequencetools.flatten_sequence(music)
        abjad> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_tokens))
        abjad> measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    ::

        abjad> f(staff)
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

    Return time-token maker.
    '''

    ### PRIVATE METHODS ###

    def _force_token_parts(self, tokens, quintuplet):
        lefts, middles, rights, left_lengths, right_lengths=quintuplet
        lefts_index, rights_index = 0, 0
        forced_tokens = []
        for token_index, token in enumerate(tokens):
            left_length = left_lengths[token_index]
            left = lefts[lefts_index:lefts_index+left_length]
            lefts_index += left_length
            right_length = right_lengths[token_index]
            right = rights[rights_index:rights_index+right_length]
            rights_index += right_length
            available_left_length = len(token)
            left_length = min([left_length, available_left_length])
            available_right_length = len(token) - left_length
            right_length = min([right_length, available_right_length])
            middle_length = len(token) - left_length - right_length

            left = left[:left_length]
            middle = middle_length * [middles[token_index]]
            right = right[:right_length]
            left_part, middle_part, right_part = \
                sequencetools.partition_sequence_once_by_counts_without_overhang(
                token, [left_length, middle_length, right_length])
            left_part = self._force_token_part(left_part, left)
            middle_part = self._force_token_part(middle_part, middle)
            right_part = self._force_token_part(right_part, right)
            forced_token = left_part + middle_part + right_part
            forced_tokens.append(forced_token)
        unforced_weights = [mathtools.weight(x) for x in tokens]
        forced_weights = [mathtools.weight(x) for x in forced_tokens]
        assert forced_weights == unforced_weights
        return forced_tokens
