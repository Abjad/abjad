from abjad.tools.pitchtools import HarmonicDiatonicInterval


def _init_triad(quality_string):
    if quality_string == 'major':
        intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5)]
    elif quality_string == 'minor':
        intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('perfect', 5)]
    elif quality_string == 'diminished':
        intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('diminished', 5)]
    elif quality_string == 'augmented':
        intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('augmented', 5)]
    else:
        raise ValueError("unknown triad quality string '%s'." % quality_string)
    intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
    #self.extend(intervals)
    #self._quality_string = quality_string
    return intervals
