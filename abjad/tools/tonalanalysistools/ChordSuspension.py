# -*- encoding: utf-8 -*-
import re
from abjad.tools.abctools import AbjadObject


class ChordSuspension(AbjadObject):
    '''A chord of 9-8, 7-6, 4-3, 2-1 and other types of
    suspension typical of, for example, the Bach chorales.

    ::

        >>> suspension = tonalanalysistools.ChordSuspension(4, 3)
        >>> suspension
        ChordSuspension(ScaleDegree('4'), ScaleDegree('3'))

    Value object that can not be changed after instantiation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start', 
        '_stop',
        )

    _symbolic_string_regex = re.compile(r'([#|b]?\d+)-([#|b]?\d+)')

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 0:
            start, stop = self._initialize_empty()
        elif len(args) == 1 and args[0] in (None, ''):
            start, stop = self._initialize_empty()
        elif len(args) == 1 and isinstance(args[0], type(self)):
            start, stop = self._initialize_by_reference(*args)
        elif len(args) == 1 and isinstance(args[0], str):
            start, stop = self._initialize_by_symbolic_string(*args)
        elif len(args) == 1 and isinstance(args[0], tuple):
            start, stop = self._initialize_by_pair(*args)
        elif len(args) == 2:
            start, stop = self._initialize_by_start_and_stop(*args)
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, args)
            raise ValueError(message)
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''True when `arg` is a chord suspension when start and stop equal to
        those of this chord suspension. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.start == arg.start:
                if self.stop == arg.stop:
                    return True
        return False

    def __ne__(self, arg):
        r'''True when `arg` does not equal chord suspension. Otherwise false.

        Returns boolean.
        '''
        return not self == arg

    def __str__(self):
        r'''String representation of chord suspension.

        Returns string.
        '''
        if self.start is not None and self.stop is not None:
            return '{!s}-{!s}'.format(self.start, self.stop)
        else:
            return ''

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = []
        if self.start is not None and self.stop is not None:
            positional_argument_values.append(self.start)
            positional_argument_values.append(self.stop)
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            )

    ### PRIVATE METHODS ###

    def _initialize_by_pair(self, pair):
        start, stop = pair
        return self._initialize_by_start_and_stop(start, stop)

    def _initialize_by_reference(self, chord_suspension):
        start, stop = chord_suspension.start, chord_suspension.stop
        return self._initialize_by_start_and_stop(start, stop)

    def _initialize_by_start_and_stop(self, start, stop):
        from abjad.tools import tonalanalysistools
        start = tonalanalysistools.ScaleDegree(start)
        stop = tonalanalysistools.ScaleDegree(stop)
        return start, stop

    def _initialize_by_symbolic_string(self, symbolic_string):
        from abjad.tools import tonalanalysistools
        groups = self._symbolic_string_regex.match(symbolic_string).groups()
        start, stop = groups
        start = tonalanalysistools.ScaleDegree(start)
        stop = tonalanalysistools.ScaleDegree(stop)
        return start, stop

    def _initialize_empty(self):
        return None, None

    ### PUBLIC PROPERTIES ###

    @property
    def chord_name(self):
        r'''Chord name of suspension.

        ::

            >>> suspension.chord_name
            'sus4'

        Returns string.
        '''
        if self.is_empty:
            return ''
        return 'sus{!s}'.format(self.start)

    @property
    def figured_bass_pair(self):
        r'''Figured bass pair of suspension.

        ::

            >>> suspension.figured_bass_pair
            (4, 3)

        Returns integer pair.
        '''
        return self.start.number, self.stop.number

    @property
    def figured_bass_string(self):
        r'''Figured bass string.

        ::

            >>> suspension.figured_bass_string
            '4-3'

        Returns string.
        '''
        if self.is_empty:
            return ''
        return '{!s}-{!s}'.format(self.start, self.stop)

    @property
    def is_empty(self):
        r'''True when start and stop are none. Otherwise false.

        ::

            >>> suspension.is_empty
            False

        '''
        return self.start is None and self.stop is None

    @property
    def start(self):
        r'''Start of suspension.

        ::

            >>> suspension.start
            ScaleDegree(4)

        Returns scale degree.
        '''
        return self._start

    @property
    def stop(self):
        r'''Stop of suspension.

        ::

            >>> suspension.stop
            ScaleDegree(3)

        Returns scale degree.
        '''
        return self._stop
        

    @property
    def title_string(self):
        r'''Title string of suspension.

        ::

            >>> suspension.title_string
            'FourThreeSuspension'

        Returns string.
        '''
        if self.is_empty:
            return ''
        start = self.start.title_string
        stop = self.stop.title_string
        return '{!s}{!s}Suspension'.format(start, stop)
