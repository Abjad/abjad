# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class TerracedDynamicsHandler(DynamicHandler):
    r'''Terraced dynamics handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_always_first_note',
        '_dynamics',
        '_minimum_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        always_first_note=True,
        dynamics=None, 
        minimum_duration=None,
        ):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        assert isinstance(always_first_note, bool), repr(always_first_note)
        self._always_first_note = always_first_note
        if dynamics is not None:
            for dynamic in dynamics:
                if not indicatortools.Dynamic.is_dynamic_name(dynamic):
                    message = 'not dynamic name: {!r}.'
                    message = message.format(dynamic)
                    raise TypeError(message)
        self._dynamics = dynamics

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties, timespan=None, offset=0):
        r'''Calls handler on `expr` with keywords.

        Returns none.
        '''
        dynamics = datastructuretools.CyclicTuple(self.dynamics)
        for i, logical_tie in enumerate(logical_ties):
            dynamic_name = dynamics[offset + i]
            if i == 0 and self.always_first_note:
                pass
            elif self.minimum_duration is not None:
                written_duration = durationtools.Duration(0)
                for note in logical_tie:
                    written_duration += note.written_duration
                if written_duration < self.minimum_duration:
                    continue
            #indicatortools.Dynamic(dynamic_name)(note_or_chord)
            command = indicatortools.LilyPondCommand(dynamic_name, 'right')
            attach(command, logical_tie.head)

    ### PUBLIC PROPERTIES ###

    @property
    def always_first_note(self):
        r'''Is true when handler should always affix dynamic to first note,
        regardless of minimum duration. Otherwise false.

        Set to true or false.
        '''
        return self._always_first_note

    @property
    def dynamics(self):
        r'''Gets dynamics of handler.

        Set to strings or none.
        '''
        return self._dynamics