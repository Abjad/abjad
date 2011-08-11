from abjad.tools.pitchtools import HarmonicDiatonicInterval


def _init_seventh(quality_string):
    if quality_string == 'dominant':
        intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('minor', 7)]
    elif quality_string == 'major':
        intervals = [HarmonicDiatonicInterval('major', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('major', 7)]
    elif quality_string == 'minor':
        intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('minor', 7)]
    elif quality_string in ('diminished', 'fully diminished'):
        intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('diminished', 5),
            HarmonicDiatonicInterval('diminished', 7)]
    elif quality_string == 'half diminished':
        intervals = [HarmonicDiatonicInterval('minor', 3),
            HarmonicDiatonicInterval('perfect', 5),
            HarmonicDiatonicInterval('diminished', 7)]
    else:
        raise ValueError("unknown seventh quality string '%s'." % quality_string)
    intervals.insert(0, HarmonicDiatonicInterval('perfect', 1))
    #self.extend(intervals)
    #self._quality_string = quality_string
    return intervals
