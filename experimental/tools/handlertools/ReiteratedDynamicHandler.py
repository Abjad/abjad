# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import iterationtools
from abjad.tools import marktools
from abjad.tools.functiontools import attach
from experimental.tools.handlertools.DynamicHandler import DynamicHandler


class ReiteratedDynamicHandler(DynamicHandler):

    ### INITIALIZER ###

    def __init__(self, dynamic_name=None, minimum_duration=None):
        DynamicHandler.__init__(self, minimum_duration=minimum_duration)
        self.dynamic_name = dynamic_name

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        for note_or_chord in \
            iterationtools.iterate_notes_and_chords_in_expr(expr):
            #marktools.DynamicMark(self.dynamic_name)(note_or_chord)
            command = marktools.LilyPondCommandMark(self.dynamic_name, 'right')
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
            elif marktools.DynamicMark.is_dynamic_name(dynamic_name):
                self._dynamic_name = dynamic_name
            else:
                raise TypeError(dynamic_name)
        return property(**locals())
