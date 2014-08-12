# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
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
        '_dynamics',
        )

    ### INITIALIZER ###

    def __init__(self, dynamics=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if dynamics is not None:
            for dynamic in dynamics:
                if not indicatortools.Dynamic.is_dynamic_name(dynamic):
                    message = 'not dynamic name: {!r}.'.format(dynamic)
                    raise TypeError(message)
        self._dynamics = dynamics

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0):
        r'''Calls handler on `expr` with keywords.

        Returns none.
        '''
        dynamics = datastructuretools.CyclicTuple(self.dynamics)
        for i, note_or_chord in enumerate(
            iterate(expr).by_class((scoretools.Note, scoretools.Chord))):
            dynamic_name = dynamics[offset + i]
            if self.minimum_duration is None or \
                self.minimum_duration <= note_or_chord._get_duration():
                #indicatortools.Dynamic(dynamic_name)(note_or_chord)
                command = indicatortools.LilyPondCommand(dynamic_name, 'right')
                attach(command, note_or_chord)
        return expr

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='dynamics',
                command='dy',
                editor=idetools.getters.get_dynamics,
                ),
            systemtools.AttributeDetail(
                name='minimum_duration',
                command='md',
                editor=idetools.getters.get_duration,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def dynamics(self):
        r'''Gets dynamics of handler.

        Returns tuple of strings or none.
        '''
        return self._dynamics