# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject
from abjad.tools import sequencetools
from abjad.tools import pitchtools


class Mode(AbjadObject):
    '''A diatonic mode.
    
    Can be extended for nondiatonic mode.

    Modes with different ascending and descending forms not yet implemented.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_named_interval_segment',
        '_mode_name',
        )

    _default_positional_input_arguments = (
        repr('dorian'),
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        if isinstance(arg, str):
            mode_name = arg
        elif isinstance(arg, Mode):
            mode_name = arg.mode_name
        else:
            message = 'must be mode or mode name: {!r}.'.format(arg)
            raise TypeError(message)
        mdi_segment = self._init_with_mode_name(mode_name)
        self._named_interval_segment = mdi_segment
        self._mode_name = mode_name

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if not isinstance(arg, type(self)):
            return False
        return self.mode_name == arg.mode_name

    def __len__(self):
        return len(self.named_interval_segment)

    def __ne__(self, arg):
        return not self == arg

    def __str__(self):
        return self.mode_name

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                self.mode_name,
                )
            )

    ### PRIVATE METHODS ###

    def _init_with_mode_name(self, mode_name):
        mdi_segment = []
        m2 = pitchtools.NamedInterval('minor', 2)
        M2 = pitchtools.NamedInterval('major', 2)
        A2 = pitchtools.NamedInterval('augmented', 2)
        dorian = [M2, m2, M2, M2, M2, m2, M2]
        if mode_name == 'dorian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, 0))
        elif mode_name == 'phrygian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -1))
        elif mode_name == 'lydian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -2))
        elif mode_name == 'mixolydian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -3))
        elif mode_name in ('aeolian', 'minor', 'natural minor'):
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -4))
        elif mode_name == 'locrian':
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -5))
        elif mode_name in ('ionian', 'major'):
            mdi_segment.extend(sequencetools.rotate_sequence(dorian, -6))
        elif mode_name == 'melodic minor':
            mdi_segment.extend([M2, m2, M2, M2, M2, M2, m2])
        elif mode_name == 'harmonic minor':
            mdi_segment.extend([M2, m2, M2, M2, m2, A2, m2])
        else:
            message = 'unknown mode name: {!r}.'.format(mode_name)
            raise ValueError(message)
        return pitchtools.IntervalSegment(
            tokens=mdi_segment,
            item_class=pitchtools.NamedInterval,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def named_interval_segment(self):
        return self._named_interval_segment

    @property
    def mode_name(self):
        return self._mode_name
