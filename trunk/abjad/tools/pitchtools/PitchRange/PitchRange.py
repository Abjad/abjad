from abjad.core import _Immutable
import numbers


class PitchRange(_Immutable):
    r""".. versionadded:: 2.0

    Abjad model of pitch range::

        abjad> pitchtools.PitchRange(-12, 36)
        PitchRange((NamedChromaticPitch('c'), 'inclusive'), (NamedChromaticPitch("c''''"), 'inclusive'))

    Init from pitch numbers, pitch instances or other pitch range objects.

    Pitch ranges implement all six Python rich comparators.

    Pitch ranges are immutable.
    """

    def __init__(self, *args):
        from abjad.tools import pitchtools
        if len(args) == 0:
            object.__setattr__(self, '_start', None)
            object.__setattr__(self, '_stop', None)
        elif len(args) == 1 and isinstance(args[0], type(self)):
            if args[0].start_pitch_is_included_in_range:
                indicator = 'inclusive'
            else:
                indicator = 'exclusive'
            start = (args[0].start_pitch, indicator)
            object.__setattr__(self, '_start', start)
            assert isinstance(args[0], type(self))
            if args[0].stop_pitch_is_included_in_range:
                indicator = 'inclusive'
            else:
                indicator = 'exclusive'
            stop = (args[0].stop_pitch, indicator)
            object.__setattr__(self, '_stop', stop)
        elif len(args) == 1 and isinstance(args[0], (tuple, list)):
            start, stop = args[0]
            type(self).__init__(self, start, stop)
        else:
            assert len(args) == 2
            start, stop = args
            if start is None:
                start = start
            elif isinstance(start, (int, long, float)):
                pitch = pitchtools.NamedChromaticPitch(start)
                start = (pitch, 'inclusive')
            else:
                assert len(start) == 2
                pitch, containment = start
                assert containment in ('inclusive', 'exclusive')
                pitch = pitchtools.NamedChromaticPitch(pitch)
                start = (pitch, containment)
            object.__setattr__(self, '_start', start)
            if stop is None:
                stop = stop
            elif isinstance(stop, (int, long, float)):
                pitch = pitchtools.NamedChromaticPitch(stop)
                stop = (pitch, 'inclusive')
            else:
                assert len(stop) == 2
                pitch, containment = stop
                assert containment in ('inclusive', 'exclusive')
                pitch = pitchtools.NamedChromaticPitch(pitch)
                stop = (pitch, containment)
            object.__setattr__(self, '_stop', stop)

    ### OVERLOADS ###

    def __contains__(self, arg):
        from abjad.tools import containertools
        from abjad.tools import pitchtools
        from abjad.tools import resttools
        from abjad.tools import skiptools
        from abjad.tools.chordtools.Chord import Chord
        from abjad.tools.notetools.Note import Note
        if getattr(arg, 'written_pitch_indication_is_nonsemantic', False):
            return True
        elif isinstance(arg, (int, long, float)):
            pitch = pitchtools.NamedChromaticPitch(arg)
            return self._contains_pitch(pitch)
        elif isinstance(arg, pitchtools.NamedChromaticPitch):
            return self._contains_pitch(arg)
        elif isinstance(arg, Note):
            return self._contains_pitch(arg.sounding_pitch)
        elif isinstance(arg, Chord):
            return all([self._contains_pitch(x) for x in arg.sounding_pitches])
        elif isinstance(arg, (resttools.Rest, skiptools.Skip)):
            return True
        elif isinstance(arg, containertools.Container):
            return all([x in self for x in arg.leaves])
        else:
            pitches = pitchtools.list_named_chromatic_pitches_in_expr(arg)
            if pitches:
                return all([self._contains_pitch(x) for x in pitches])
            else:
                try:
                    return all([self._contains_pitch(x) for x in arg])
                except TypeError:
                    return False
        return False

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self._start == arg._start:
                if self._stop == arg._stop:
                    return True
        return False

    def __ge__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.start_pitch is None:
                return False
            return pitch <= self.start_pitch
        except (TypeError, ValueError):
            return False

    def __gt__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.start_pitch is None:
                return False
            return pitch < self.start_pitch
        except (TypeError, ValueError):
            return False

    def __le__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch <= pitch
        except (TypeError, ValueError):
            return False

    def __lt__(self, arg):
        from abjad.tools import pitchtools
        try:
            pitch = pitchtools.NamedChromaticPitch(arg)
            if self.stop_pitch is None:
                return False
            return self.stop_pitch < pitch
        except (TypeError, ValueError):
            return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__, self._start, self._stop)

    ### PRIVATE METHODS ###

    def _contains_pitch(self, pitch):
        from abjad.tools import pitchtools
        if isinstance(pitch, numbers.Number):
            #pitch = pitchtools.NumberedChromaticPitch(pitch)
            pitch = pitchtools.NamedChromaticPitch(pitch)
        elif isinstance(pitch, str):
            pitch = pitchtools.NamedChromaticPitch(pitch)
        if self._start is None and self._stop is None:
            return True
        elif self._start is None:
            if self.stop_pitch_is_included_in_range:
                return pitch <= self.stop_pitch
            else:
                return pitch < self.stop_pitch
        elif self._stop is None:
            if self.start_pitch_is_included_in_range:
                return self.start_pitch <= pitch
            else:
                return self.start_pitch < pitch
        else:
            if self.start_pitch_is_included_in_range:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch <= pitch <= self.stop_pitch
                else:
                    return self.start_pitch <= pitch < self.stop_pitch
            else:
                if self.stop_pitch_is_included_in_range:
                    return self.start_pitch < pitch <= self.stop_pitch
                else:
                    return self.start_pitch < pitch < self.stop_pitch

    ### PUBLIC ATTRIBUTES ###

    @property
    def start_pitch(self):
        r'''Read-only start pitch of range::

            abjad> pitch_range = pitchtools.PitchRange(-12, 36)
            abjad> pitch_range.start_pitch
            NamedChromaticPitch('c')

        Return pitch.
        '''
        if self._start is None:
            return None
        return self._start[0]

    @property
    def start_pitch_is_included_in_range(self):
        '''True when start pitch is included in range. Otherwise false::

            abjad> pitch_range = pitchtools.PitchRange(-12, 36)
            abjad> pitch_range.start_pitch_is_included_in_range
            True

        Return boolean.
        '''
        if self._start is None:
            return True
        return self._start[1] == 'inclusive'

    @property
    def stop_pitch(self):
        r"""Read-only stop pitch of range::

            abjad> pitch_range = pitchtools.PitchRange(-12, 36)
            abjad> pitch_range.stop_pitch
            NamedChromaticPitch("c''''")

        Return pitch.
        """
        if self._stop is None:
            return None
        return self._stop[0]

    @property
    def stop_pitch_is_included_in_range(self):
        '''True when stop pitch is included in range. Otherwise false::

            abjad> pitch_range = pitchtools.PitchRange(-12, 36)
            abjad> pitch_range.stop_pitch_is_included_in_range
            True

        Return boolean.
        '''
        if self._stop is None:
            return True
        return self._stop[1] == 'inclusive'
