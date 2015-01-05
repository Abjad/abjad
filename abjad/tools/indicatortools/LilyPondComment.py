# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class LilyPondComment(AbjadValueObject):
    r'''A LilyPond comment.

    ::

        >>> note = Note("c'4")
        >>> comment = indicatortools.LilyPondComment('this is a comment')
        >>> attach(comment, note)
        >>> show(note) # doctest: +SKIP

    ..  doctest::

        >>> print(format(note))
        % this is a comment
        c'4

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents_string',
        '_format_slot',
        )

    _format_leaf_children = False

    _valid_format_slots = (
        'before',
        'after',
        'opening',
        'closing',
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
        format_slot = format_slot or 'before'
        self._contents_string = contents_string
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string format of LilyPond comment.

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

        ::

            >>> comment.contents_string
            'this is a comment'

        Returns string.
        '''
        return self._contents_string

    @property
    def format_slot(self):
        r'''Format slot of LilyPond comment.

        ::

            >>> comment.format_slot
            'before'

        Returns string.
        '''
        return self._format_slot