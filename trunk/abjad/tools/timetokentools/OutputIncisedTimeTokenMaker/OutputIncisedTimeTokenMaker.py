from abjad.tools.timetokentools.IncisedTimeTokenMaker import IncisedTimeTokenMaker


class OutputIncisedTimeTokenMaker(IncisedTimeTokenMaker):
    '''.. versionadded:: 2.8

    Abstract base class for time token makers that incise only the 
    first and last time tokens they produce.
    '''

    ### PRIVATE METHODS ###

    def _make_numeric_map(self, duration_pairs,
        prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, prolation_addenda):
        numeric_map, prefix_signal_index, suffix_signal_index = [], 0, 0
        prefix_length, suffix_length = prefix_lengths[0], suffix_lengths[0]
        prefix = prefix_signal[prefix_signal_index:prefix_signal_index+prefix_length]
        suffix = suffix_signal[suffix_signal_index:suffix_signal_index+suffix_length]
        if len(duration_pairs) == 1:
            prolation_addendum = prolation_addenda[0]
            numerator = duration_pairs[0][0]
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(numerator, prefix, suffix)
            numeric_map.append(numeric_map_part)
        else:
            prolation_addendum = prolation_addenda[0]
            numerator = duration_pairs[0][0]
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(numerator, prefix, ())
            numeric_map.append(numeric_map_part)
            for i, duration_pair in enumerate(duration_pairs[1:-1]):
                prolation_addendum = prolation_addenda[i+1]
                numerator = duration_pair[0]
                numerator += (prolation_addendum % numerator)
                numeric_map_part = self._make_numeric_map_part(numerator, (), ())
                numeric_map.append(numeric_map_part)
            try:
                prolation_addendum = prolation_addenda[i+2]
            except UnboundLocalError:
                prolation_addendum = prolation_addenda[1+2]
            numerator = duration_pairs[-1][0]
            numerator += (prolation_addendum % numerator)
            numeric_map_part = self._make_numeric_map_part(numerator, (), suffix)
            numeric_map.append(numeric_map_part)
        return numeric_map
