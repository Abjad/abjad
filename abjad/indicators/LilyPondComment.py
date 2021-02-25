from ..bundle import LilyPondFormatBundle
from ..storage import StorageFormatManager


class LilyPondComment:
    r"""
    LilyPond comment.

    ..  container:: example

        Two-word comment:

        >>> note = abjad.Note("c'4")
        >>> comment = abjad.LilyPondComment('a comment')
        >>> abjad.attach(comment, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            % a comment
            c'4

    ..  container:: example

        Three-word comment:

        >>> note = abjad.Note("c'4")
        >>> comment = abjad.LilyPondComment('yet another comment')
        >>> abjad.attach(comment, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(note)
            >>> print(string)
            % yet another comment
            c'4

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_string", "_format_slot")

    _allowable_format_slots = ("after", "before", "closing", "opening")

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(self, string: str = None, format_slot: str = "before") -> None:
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

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

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
        return rf"% {self.string}"

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
    def tweaks(self) -> None:
        """
        Are not implemented on LilyPond comment.
        """
        pass
