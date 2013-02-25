from abjad.tools import mathtools
from abjad.tools.rhythmmakertools.IncisedRhythmMaker import IncisedRhythmMaker


class DivisionIncisedRhythmMaker(IncisedRhythmMaker):
    '''.. versionadded:: 2.8

    Abstract base class for rhythm-makers that incise every output cell they produce.
    '''

    ### PRIVATE METHODS ###

    def _make_numeric_map(self, duration_pairs=None,
        prefix_talea=None, prefix_lengths=None,
        suffix_talea=None, suffix_lengths=None, prolation_addenda=None):
        numeric_map, prefix_talea_index, suffix_talea_index = [], 0, 0
        for pair_index, duration_pair in enumerate(duration_pairs):
            prefix_length, suffix_length = prefix_lengths[pair_index], suffix_lengths[pair_index]
            prefix = prefix_talea[prefix_talea_index:prefix_talea_index+prefix_length]
            suffix = suffix_talea[suffix_talea_index:suffix_talea_index+suffix_length]
            prefix_talea_index += prefix_length
            suffix_talea_index += suffix_length
            prolation_addendum = prolation_addenda[pair_index]
            if isinstance(duration_pair, tuple):
                numerator = duration_pair[0] + (prolation_addendum % duration_pair[0])
            else:
                numerator = duration_pair.numerator + (prolation_addendum % duration_pair.numerator)
            numeric_map_part = self._make_numeric_map_part(numerator, prefix, suffix)
            numeric_map.append(numeric_map_part)
        return numeric_map
