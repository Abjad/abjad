# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from experimental.tools.handlertools.DynamicHandler import DynamicHandler


class ReiteratedDynamicHandler(DynamicHandler):

    ### INITIALIZER ###

    def __init__(self, dynamic_name=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        self.dynamic_name = dynamic_name

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for note_or_chord in \
            iterate(expr).by_class((scoretools.Note, scoretools.Chord)):
            #indicatortools.Dynamic(self.dynamic_name)(note_or_chord)
            command = indicatortools.LilyPondCommand(self.dynamic_name, 'right')
            attach(command, note_or_chord)
        return expr

    ### PUBLIC PROPERTIES ###

    @apply
    def dynamic_name():
        def fget(self):
            return self._dynamic_name
        def fset(self, dynamic_name):
            if dynamic_name is None:
                self._dynamic_name = dynamic_name
            elif indicatortools.Dynamic.is_dynamic_name(dynamic_name):
                self._dynamic_name = dynamic_name
            else:
                raise TypeError(dynamic_name)
        return property(**locals())
