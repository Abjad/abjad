# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.handlertools.DynamicHandler import DynamicHandler


class ReiteratedDynamicHandler(DynamicHandler):
    r'''Reiterated dynamic handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_dynamic_name',
        )

    ### INITIALIZER ###

    def __init__(self, dynamic_name=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        if dynamic_name is not None:
            assert indicatortools.Dynamic.is_dynamic_name(dynamic_name)
        self._dynamic_name = dynamic_name

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        for note_or_chord in \
            iterate(expr).by_class((scoretools.Note, scoretools.Chord)):
            #indicatortools.Dynamic(self.dynamic_name)(note_or_chord)
            command = indicatortools.LilyPondCommand(
                self.dynamic_name,
                'right',
                )
            attach(command, note_or_chord)
        return expr

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='dynamic_name',
                command='dy',
                editor=idetools.getters.get_dynamic,
                ),
            systemtools.AttributeDetail(
                name='minimum_duration',
                command='md',
                editor=idetools.getters.get_duration,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic_name(self):
        r'''Gets dynamic name of handler.

        Returns string or none.
        '''
        return self._dynamic_name