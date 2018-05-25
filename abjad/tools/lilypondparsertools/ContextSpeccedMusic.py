from abjad.tools import datastructuretools
from abjad.tools.lilypondparsertools.Music import Music


class ContextSpeccedMusic(Music):
    """
    Abjad model of the LilyPond AST context-specced music node.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        #'context',
        'lilypond_type',
        'music',
        'optional_id',
        'optional_context_mod',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_type=None,
        optional_id=None,
        optional_context_mod=None,
        music=None,
        ):
        from abjad.tools import lilypondparsertools
        lilypond_type = lilypond_type or ''
        music = music or lilypondparsertools.SequentialMusic()
        assert datastructuretools.String.is_string(lilypond_type)
        assert isinstance(music, Music)
        self.lilypond_type = lilypond_type
        self.optional_id = optional_id
        self.optional_context_mod = optional_context_mod
        self.music = music

    ### PUBLIC METHODS ###

    def construct(self):
        """
        Constructs context.

        Returns context.
        """
        if self.lilypond_type in self.known_contexts:
            context = known_contexts[self.lilypond_type]([])
        else:
            message = 'context type not supported: {}.'
            message = message.format(self.lilypond_type)
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
        """
        Known contexts.

        Returns dictionary.
        """
        return {
            'ChoirStaff': scoretools.StaffGroup,
            'GrandStaff': scoretools.StaffGroup,
            'PianoStaff': scoretools.StaffGroup,
            'Score': scoretools.Score,
            'Staff': scoretools.Staff,
            'StaffGroup': scoretools.StaffGroup,
            'Voice': scoretools.Voice,
        }
