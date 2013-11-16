# -*- encoding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadObject import AbjadObject


class LilyPondComment(AbjadObject):
    r'''A LilyPond comment.

    ::

        >>> note = Note("c'4")
        >>> comment = indicatortools.LilyPondComment('this is a comment')
        >>> attach(comment, note)
        >>> show(note) # doctest: +SKIP

    ..  doctest::

        >>> print format(note)
        % this is a comment
        c'4

    Initializes LilyPond comment from contents string;
    or contents string and format slot;
    or from other LilyPond comment;
    or from other LilyPond comment and format slot.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents_string',
        '_format_slot',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], type(self)):
            contents_string = copy.copy(args[0].contents_string)
            format_slot = copy.copy(args[0].format_slot)
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            contents_string = copy.copy(args[0])
            format_slot = None
        elif len(args) == 2 and isinstance(args[0], type(self)):
            contents_string = copy.copy(args[0].contents_string)
            format_slot = args[1]
        elif len(args) == 2 and not isinstance(args[0], type(self)):
            contents_string = args[0]
            format_slot = args[1]
        else:
            message = 'can not initialize LilyPond comment from {!r}.'
            message = message.format(args)
            raise ValueError(message)
        format_slot = format_slot or 'before'
        self._contents_string = contents_string
        self._format_slot = format_slot

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies LilyPond comment.

        Returns new LilyPond comment.
        '''
        new = type(self)(self._contents_string)
        new.format_slot = self.format_slot
        return new

    def __eq__(self, arg):
        r'''True when `arg` is a LilyPond comment with contents string
        equal to LilyPond comment. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self._contents_string == arg._contents_string
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._contents_string)

    @property
    def _lilypond_format(self):
        from abjad.tools import stringtools
        command = stringtools.snake_case_to_lower_camel_case(
            self.contents_string)
        return r'%% %s' % command

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
