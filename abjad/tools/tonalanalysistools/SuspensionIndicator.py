# -*- encoding: utf-8 -*-
import re
from abjad.tools.abctools import AbjadObject


class SuspensionIndicator(AbjadObject):
    '''An indicator of 9-8, 7-6, 4-3, 2-1 and other types of
    suspension typical of, for example, the Bach chorales.

    Value object that can not be changed after instantiation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start', 
        '_stop',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 0:
            start, stop = self._init_empty()
        elif len(args) == 1 and args[0] in (None, ''):
            start, stop = self._init_empty()
        elif len(args) == 1 and isinstance(args[0], type(self)):
            start, stop = self._init_by_reference(*args)
        elif len(args) == 1 and isinstance(args[0], str):
            start, stop = self._init_by_symbolic_string(*args)
        elif len(args) == 1 and isinstance(args[0], tuple):
            start, stop = self._init_by_pair(*args)
        elif len(args) == 2:
            start, stop = self._init_by_start_and_stop(*args)
        else:
            raise ValueError('can not initialize suspension indicator.')
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.start == arg.start:
                if self.stop == arg.stop:
                    return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        if self.start is not None and self.stop is not None:
            return '{}({}, {})'.format(type(self).__name__, self.start, self.stop)
        else:
            return '{}()'.format(type(self).__name__)

    def __str__(self):
        if self.start is not None and self.stop is not None:
            return '{}-{}'.format(self.start, self.stop)
        else:
            return ''

    ### PRIVATE PROPERTIES ###

    _symbolic_string_regex = re.compile(r'([#|b]?\d+)-([#|b]?\d+)')

    ### PRIVATE METHODS ###

    def _init_by_pair(self, pair):
        start, stop = pair
        return self._init_by_start_and_stop(start, stop)

    def _init_by_reference(self, suspension_indicator):
        start, stop = suspension_indicator.start, suspension_indicator.stop
        return self._init_by_start_and_stop(start, stop)

    def _init_by_start_and_stop(self, start, stop):
        from abjad.tools import tonalanalysistools
        start = tonalanalysistools.ScaleDegree(start)
        stop = tonalanalysistools.ScaleDegree(stop)
        return start, stop

    def _init_by_symbolic_string(self, symbolic_string):
        from abjad.tools import tonalanalysistools
        groups = self._symbolic_string_regex.match(symbolic_string).groups()
        start, stop = groups
        start = tonalanalysistools.ScaleDegree(start)
        stop = tonalanalysistools.ScaleDegree(stop)
        return start, stop

    def _init_empty(self):
        return None, None

    ### PUBLIC PROPERTIES ###

    @property
    def chord_name(self):
        if self.is_empty:
            return ''
        return 'sus{}'.format(self.start)

    @property
    def figured_bass_pair(self):
        return self.start.number, self.stop.number

    @property
    def figured_bass_string(self):
        if self.is_empty:
            return ''
        return '{}-{}'.format(self.start, self.stop)

    @property
    def is_empty(self):
        return self.start is None and self.stop is None

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    @property
    def title_string(self):
        if self.is_empty:
            return ''
        start = self.start.title_string
        stop = self.stop.title_string
        return '{}{}Suspension'.format(start, stop)
