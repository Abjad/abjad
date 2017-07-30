# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondComment(AbjadValueObject):
    r'''LilyPond comment.

    ::

        >>> import abjad

    ..  container:: example

        Two-word comment:

        ::

            >>> note = abjad.Note("c'4")
            >>> comment = abjad.LilyPondComment('a comment')
            >>> abjad.attach(comment, note)
            >>> show(note) # doctest: +SKIP

        ..  docs::

            >>> f(note)
            % a comment
            c'4

    ..  container:: example

        Three-word comment:

        ::

            >>> note = abjad.Note("c'4")
            >>> comment = abjad.LilyPondComment('yet another comment')
            >>> abjad.attach(comment, note)
            >>> show(note) # doctest: +SKIP

        ..  docs::

            >>> f(note)
            % yet another comment
            c'4

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents_string',
        '_format_slot',
        )

    _allowable_format_slots = (
        'after',
        'before',
        'closing',
        'opening',
        'right',
        )

    _can_attach_to_containers = True

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(self, contents_string=None, format_slot=None):
        if isinstance(contents_string, type(self)):
            argument = contents_string
            contents_string = argument.contents_string
            format_slot = format_slot or argument.format_slot
        else:
            contents_string = str(contents_string)
        self._contents_string = contents_string
        format_slot = format_slot or 'before'
        assert format_slot in self._allowable_format_slots, repr(format_slot)
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of LilyPond comment.

        ..  container:: example

            Two-word comment:

            ::

                >>> comment = abjad.LilyPondComment('a comment')
                >>> str(comment)
                '% a comment'

        ..  container:: example

            Three-word comment:

            ::

                >>> comment = abjad.LilyPondComment('yet another comment')
                >>> str(comment)
                '% yet another comment'

        Returns string.
        '''
        return r'% {}'.format(self.contents_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._contents_string)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        format_slot = bundle.get(self.format_slot)
        format_slot.comments.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def contents_string(self):
        r'''Contents string of LilyPond comment.

        ..  container:: example

            Two-word comment:

            ::

                >>> comment = abjad.LilyPondComment('a comment')
                >>> comment.contents_string
                'a comment'

        ..  container:: example

            Three-word comment:

            ::

                >>> comment = abjad.LilyPondComment('yet another comment')
                >>> comment.contents_string
                'yet another comment'

        Returns string.
        '''
        return self._contents_string

    @property
    def format_slot(self):
        r'''Format slot of LilyPond comment.

        ..  container:: example

            Two-word comment:

            ::

                >>> comment = abjad.LilyPondComment('a comment')
                >>> comment.format_slot
                'before'

        ..  container:: example

            Three-word comment:

            ::

                >>> comment = abjad.LilyPondComment('yet another comment')
                >>> comment.format_slot
                'before'

        Defaults to ``'before'``.

        Set to allowable format slot string.

        Returns string.
        '''
        return self._format_slot

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots():
        r'''Lists allowable format slots.

        ..  container:: example

            Default:

                >>> commands = abjad.LilyPondComment.list_allowable_format_slots()
                >>> for command in commands:
                ...     command
                'after'
                'before'
                'closing'
                'opening'
                'right'

        Returns tuple of strings.
        '''
        return LilyPondComment._allowable_format_slots
