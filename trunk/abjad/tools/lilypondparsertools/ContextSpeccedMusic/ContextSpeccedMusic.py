# -*- encoding: utf-8 -*-
from abjad.tools.lilypondparsertools.Music import Music


class ContextSpeccedMusic(Music):
    r'''Abjad model of the LilyPond AST context-specced music node.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        'context', 
        'music', 
        'optional_id', 
        'optional_context_mod',
        )

    ### INITIALIZER ###

    def __init__(self, context, optional_id, optional_context_mod, music):
        assert isinstance(context, (str, unicode))
        assert isinstance(music, Music)
        self.context_name = context
        self.optional_id = optional_id
        self.optional_context_mod = optional_context_mod
        self.music = music

    ### PUBLIC METHODS ###

    def construct(self):
        if self.context_name in self.known_contexts:
            context = known_contexts[self.context_name]([])
        else:
            message = 'context type %s not supported.'
            raise Exception(message % self.context_name)

        if self.optional_id is not None:
            context.name = self.optional_id

        if self.optional_context_mod is not None:
            for x in self.optional_context_mod:
                print x
            pass # TODO: Implement context mods on contexts. #

        if isinstance(self.music, lilypondparsertools.ParallelMusic):
            context.is_simultaneous = True
        context.extend(music.construct())

        return context

    ### PUBLIC PROPERTIES ###

    @property
    def known_contexts(self):
        return {
            'ChoirStaff': scoretools.StaffGroup,
            'GrandStaff': scoretools.GrandStaff,
            'PianoStaff': scoretools.PianoStaff,
            'Score': scoretools.Score,
            'Staff': stafftools.Staff,
            'StaffGroup': scoretools.StaffGroup,
            'Voice': voicetools.Voice,
        }
