# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.lilypondparsertools.Music import Music


class ContextSpeccedMusic(Music):
    r'''Abjad model of the LilyPond AST context-specced music node.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        #'context',
        'context_name',
        'music',
        'optional_id',
        'optional_context_mod',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        context_name=None,
        optional_id=None,
        optional_context_mod=None,
        music=None,
        ):
        from abjad.tools import lilypondparsertools
        context_name = context_name or ''
        music = music or lilypondparsertools.SequentialMusic()
        assert stringtools.is_string(context_name)
        assert isinstance(music, Music)
        self.context_name = context_name
        self.optional_id = optional_id
        self.optional_context_mod = optional_context_mod
        self.music = music

    ### PUBLIC METHODS ###

    def construct(self):
        r'''Constructs context.

        Returns context.
        '''
        if self.context_name in self.known_contexts:
            context = known_contexts[self.context_name]([])
        else:
            message = 'context type not supported: {}.'
            message = message.format(self.context_name)
            raise Exception(message)

        if self.optional_id is not None:
            context.name = self.optional_id

        if self.optional_context_mod is not None:
            for x in self.optional_context_mod:
                print(x)
            # TODO: implement context modifications on contexts
            pass

        if isinstance(self.music, lilypondparsertools.SimultaneousMusic):
            context.is_simultaneous = True
        context.extend(music.construct())

        return context

    ### PUBLIC PROPERTIES ###

    @property
    def known_contexts(self):
        r'''Known contexts.

        Returns dictionary.
        '''
        return {
            'ChoirStaff': scoretools.StaffGroup,
            'GrandStaff': scoretools.StaffGroup,
            'PianoStaff': scoretools.StaffGroup,
            'Score': scoretools.Score,
            'Staff': scoretools.Staff,
            'StaffGroup': scoretools.StaffGroup,
            'Voice': scoretools.Voice,
        }
