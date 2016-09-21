# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondComment(AbjadValueObject):
    r'''A LilyPond comment.

    ..  container:: example

        **Example 1.** Two-word comment:

        ::

            >>> note = Note("c'4")
            >>> comment = indicatortools.LilyPondComment('a comment')
            >>> attach(comment, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            % a comment
            c'4

    ..  container:: example

        **Example 2.** Three-word comment:

        ::

            >>> note = Note("c'4")
            >>> comment = indicatortools.LilyPondComment('yet another comment')
            >>> attach(comment, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            % yet another comment
            c'4

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents_string',
        '_default_scope',
        '_format_slot',
        )

    _format_leaf_children = False

    _allowable_format_slots = (
        'after',
        'before',
        'closing',
        'opening',
        'right',
        )

    ### INITIALIZER ###

    def __init__(self, contents_string=None, format_slot=None):
        if isinstance(contents_string, type(self)):
            expr = contents_string
            contents_string = expr.contents_string
            format_slot = format_slot or expr.format_slot
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

            **Example 1.** Two-word comment:

            ::

                >>> comment = indicatortools.LilyPondComment('a comment')
                >>> str(comment)
                '% a comment'

        ..  container:: example

            **Example 2.** Three-word comment:

            ::

                >>> comment = indicatortools.LilyPondComment('yet another comment')
                >>> str(comment)
                '% yet another comment'

        Returns string.
        '''
        return r'% {}'.format(self.contents_string)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        format_slot = lilypond_format_bundle.get(self.format_slot)
        format_slot.comments.append(str(self))
        return lilypond_format_bundle

    ### PUBLIC METHODS ###

    @staticmethod
    def list_allowable_format_slots():
        r'''Lists allowable format slots.

        ..  container:: example

            **Example 1.** Default:

                >>> commands = indicatortools.LilyPondComment.list_allowable_format_slots()
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

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._contents_string)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def contents_string(self):
        r'''Contents string of LilyPond comment.

        ..  container:: example

            **Example 1.** Two-word comment:

            ::

                >>> comment = indicatortools.LilyPondComment('a comment')
                >>> comment.contents_string
                'a comment'

        ..  container:: example

            **Example 2.** Three-word comment:

            ::

                >>> comment = indicatortools.LilyPondComment('yet another comment')
                >>> comment.contents_string
                'yet another comment'

        Returns string.
        '''
        return self._contents_string

    @property
    def format_slot(self):
        r'''Format slot of LilyPond comment.

        ..  container:: example

            **Example 1.** Two-word comment:

            ::

                >>> comment = indicatortools.LilyPondComment('a comment')
                >>> comment.format_slot
                'before'

        ..  container:: example

            **Example 2.** Three-word comment:

            ::

                >>> comment = indicatortools.LilyPondComment('yet another comment')
                >>> comment.format_slot
                'before'

        Defaults to ``'before'``.

        Set to allowable format slot string.

        Returns string.
        '''
        return self._format_slot
