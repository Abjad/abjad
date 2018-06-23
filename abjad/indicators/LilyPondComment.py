import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class LilyPondComment(AbjadValueObject):
    r"""
    LilyPond comment.

    ..  container:: example

        Two-word comment:

        >>> note = abjad.Note("c'4")
        >>> comment = abjad.LilyPondComment('a comment')
        >>> abjad.attach(comment, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            % a comment
            c'4

    ..  container:: example

        Three-word comment:

        >>> note = abjad.Note("c'4")
        >>> comment = abjad.LilyPondComment('yet another comment')
        >>> abjad.attach(comment, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            % yet another comment
            c'4

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_string',
        '_format_slot',
        )

    _allowable_format_slots = (
        'after',
        'before',
        'closing',
        'opening',
        )

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        string: str = None,
        format_slot: str = 'before',
        ) -> None:
        if isinstance(string, type(self)):
            argument = string
            string = argument.string
            format_slot = format_slot or argument.format_slot
        else:
            string = str(string)
        self._string = string
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        """
        Gets string representation of LilyPond comment.

        ..  container:: example

            Two-word comment:

            >>> comment = abjad.LilyPondComment('a comment')
            >>> str(comment)
            '% a comment'

        ..  container:: example

            Three-word comment:

            >>> comment = abjad.LilyPondComment('yet another comment')
            >>> str(comment)
            '% yet another comment'

        """
        return rf'% {self.string}'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        format_slot.comments.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def string(self) -> str:
        """
        Gets string.

        ..  container:: example

            Two-word comment:

            >>> comment = abjad.LilyPondComment('a comment')
            >>> comment.string
            'a comment'

        ..  container:: example

            Three-word comment:

            >>> comment = abjad.LilyPondComment('yet another comment')
            >>> comment.string
            'yet another comment'

        """
        return self._string

    @property
    def format_slot(self) -> str:
        """
        Format slot of LilyPond comment.

        ..  container:: example

            Two-word comment:

            >>> comment = abjad.LilyPondComment('a comment')
            >>> comment.format_slot
            'before'

        ..  container:: example

            Three-word comment:

            >>> comment = abjad.LilyPondComment('yet another comment')
            >>> comment.format_slot
            'before'

        """
        return self._format_slot

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on LilyPond comment.
        """
        pass

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots() -> typing.Tuple[str, ...]:
        """
        Lists allowable format slots.

        ..  container:: example

            >>> commands = abjad.LilyPondComment.list_allowable_format_slots()
            >>> for command in commands:
            ...     command
            ...
            'after'
            'before'
            'closing'
            'opening'

        """
        return LilyPondComment._allowable_format_slots
