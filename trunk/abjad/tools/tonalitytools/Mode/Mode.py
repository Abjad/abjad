from abjad.core import _Immutable
from abjad.tools import sequencetools
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval
from abjad.tools.pitchtools.MelodicDiatonicIntervalSegment import MelodicDiatonicIntervalSegment


class Mode(_Immutable):
    '''.. versionadded:: 2.0

    Diatonic mode. Can be extended for nondiatonic mode.

    Modes with different ascending and descending forms not yet implemented.
    '''

    def __init__(self, arg):
        if isinstance(arg, str):
            #self._init_with_mode_name(arg)
            mode_name = arg
        elif isinstance(arg, Mode):
            #self._init_with_mode_name(arg.mode_name)
            mode_name = arg.mode_name
        else:
            raise TypeError('%s must be mode instance or mode name.' % arg)
        mdi_segment = self._init_with_mode_name(mode_name)
        object.__setattr__(self, '_melodic_diatonic_interval_segment', mdi_segment)
        object.__setattr__(self, '_mode_name', mode_name)

    ### OVERLOADS ###

    def __eq__(self, arg):
        if not isinstance(arg, type(self)):
            return False
        return self.mode_name == arg.mode_name

    def __len__(self):
        return len(self.melodic_diatonic_interval_segment)

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self.mode_name)

    def __str__(self):
        return self.mode_name

    ### PRIVATE METHODS ###

    def _init_with_mode_name(self, mode_name):
        #mdi_segment = MelodicDiatonicIntervalSegment([])
        mdi_segment = []
        m2 = MelodicDiatonicInterval('minor', 2)
        M2 = MelodicDiatonicInterval('major', 2)
        dorian = [M2, m2, M2, M2, M2, m2, M2]
        if mode_name == 'dorian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, 0))
        elif mode_name == 'phrygian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -1))
        elif mode_name == 'lydian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -2))
        elif mode_name == 'mixolydian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -3))
        elif mode_name in ('aeolian', 'minor'):
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -4))
        elif mode_name == 'locrian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -5))
        elif mode_name in ('ionian', 'major'):
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -6))
        else:
            raise ValueError("unknown mode name '%s'." % mode_name)
        #self._mode_name = mode_name
        #self._melodic_diatonic_interval_segment = MelodicDiatonicIntervalSegment(mdi_segment)
        return MelodicDiatonicIntervalSegment(mdi_segment)

    ### PUBLIC ATTRIBUTES ###

    @property
    def melodic_diatonic_interval_segment(self):
        return self._melodic_diatonic_interval_segment

    @property
    def mode_name(self):
        return self._mode_name
