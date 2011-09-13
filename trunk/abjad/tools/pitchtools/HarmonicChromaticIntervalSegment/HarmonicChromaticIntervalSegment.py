from abjad.tools.pitchtools._IntervalSegment import _IntervalSegment


class HarmonicChromaticIntervalSegment(_IntervalSegment):
    '''.. versionadded:: 2.0

    Abjad model of harmonic chromatic interval segment::

        abjad> pitchtools.HarmonicChromaticIntervalSegment([10, -12, -13, -13.5])
        HarmonicChromaticIntervalSegment(10, 12, 13, 13.5)

    Harmonic chromatic interval segments are immutable.
    '''

    def __new__(self, hci_tokens):
        from abjad.tools import pitchtools
        hcis = []
        for token in hci_tokens:
            hci = pitchtools.HarmonicChromaticInterval(token)
            hcis.append(hci)
        return tuple.__new__(self, hcis)
