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

    def __init__(self, dynamics=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if dynamics is None:
            dynamics = []
        self.dynamics = dynamics

    ### SPECIAL METHODS ###

    def __call__(self, expr, offset=0):
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

    ###  PUBLIC PROPERTIES ###

    @property
    def dynamics(self):
        return self._dynamics

    @dynamics.setter
    def dynamics(self, dynamics):
        if dynamics is None:
            self._dynamics = dynamics
        elif all(
            indicatortools.Dynamic.is_dynamic_name(x) for x in dynamics):
            self._dynamics = dynamics
        else:
            raise TypeError(dynamics)