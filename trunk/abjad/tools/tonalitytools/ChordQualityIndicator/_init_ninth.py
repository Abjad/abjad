from abjad.tools.pitchtools import HarmonicDiatonicInterval


def _init_ninth(quality_string):
    if quality_string == 'dominant':
        intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('minor', 7),
            HarmonicDiatonicInterval('major', 9)]
    else:
        raise ValueError("unknown ninth quality string '%s'." % quality_string)
    intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
    #self.extend(intervals)
    #self._quality_string = quality_string
    return intervals
