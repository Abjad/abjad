from abjad import utilities
from .Music import Music


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
        from abjad import parser as abjad_parser
        lilypond_type = lilypond_type or ''
        music = music or abjad_parser.SequentialMusic()
        assert utilities.String.is_string(lilypond_type)
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

        if isinstance(self.music, abjad_parser.SimultaneousMusic):
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
        from abjad import core
        return {
            'ChoirStaff': core.StaffGroup,
            'GrandStaff': core.StaffGroup,
            'PianoStaff': core.StaffGroup,
            'Score': core.Score,
            'Staff': core.Staff,
            'StaffGroup': core.StaffGroup,
            'Voice': core.Voice,
        }
