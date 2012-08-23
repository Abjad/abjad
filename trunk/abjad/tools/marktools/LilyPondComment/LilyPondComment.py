from abjad.tools.componenttools.Component import Component
from abjad.tools.marktools.Mark import Mark
import copy


class LilyPondComment(Mark):
    r'''.. versionadded:: 2.0
    
    .. versionchanged:: 2.3
        Changed ``Comment`` to ``LilyPondComment``.

    User-defined comment::

        >>> note = Note("c'4")

    ::

        >>> marktools.LilyPondComment('this is a comment')(note)
        LilyPondComment('this is a comment')(c'4)

    ::

        >>> f(note)
        % this is a comment
        c'4

    Initialize LilyPond comment from contents string; or contents string and format
    slot; or from other LilyPond comment; or from other LilyPond comment and format
    slot.

    LilyPond comments implement ``__slots__``.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_contents_string', '_format_slot', )

    ### INITIALIZER ###

    def __init__(self, *args):
        Mark.__init__(self)
        if len(args) == 1 and isinstance(args[0], type(self)):
            self.contents_string = copy.copy(args[0].contents_string)
            self.format_slot = copy.copy(args[0].format_slot)
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self.contents_string = copy.copy(args[0])
            self.format_slot = None
        elif len(args) == 2 and isinstance(args[0], type(self)):
            self.contents_string = copy.copy(args[0].contents_string)
            self.format_slot = args[1]
        elif len(args) == 2 and not isinstance(args[0], type(self)):
            self.contents_string = args[0]
            self.format_slot = args[1]
        else:
            raise ValueError('Can not initialize LilyPond comment.')

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        #return type(self)(self._contents_string)
        new = type(self)(self._contents_string)
        new.format_slot = self.format_slot
        return new

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._contents_string == arg._contents_string
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self._contents_string)

    ### PUBLIC PROPERTIES ###

    @apply
    def contents_string():
        def fget(self):
            r'''Get contents string of comment::

                >>> comment = marktools.LilyPondComment('comment contents string')
                >>> comment.contents_string
                'comment contents string'

            Set contents string of comment::

                >>> comment.contents_string = 'new comment contents string'
                >>> comment.contents_string
                'new comment contents string'

            Set string.
            '''
            return self._contents_string
        def fset(self, contents_string):
            assert isinstance(contents_string, str)
            self._contents_string = contents_string
        return property(**locals())

    @property
    def lilypond_format(self):
        '''Read-only LilyPond input format of comment:

        ::

            >>> comment = marktools.LilyPondComment('this is a comment.')
            >>> comment.lilypond_format
            '% this is a comment.'

        Return string.
        '''
        from abjad.tools import stringtools
        command = stringtools.underscore_delimited_lowercase_to_lowercamelcase(self.contents_string)
        return r'%% %s' % command

    @apply
    def format_slot():
        def fget(self):
            '''.. versionadded:: 2.3

            Get format slot of LilyPond comment::
            
                >>> note = Note("c'4")
                >>> lilypond_comment = marktools.LilyPondComment('comment')
                >>> lilypond_comment.format_slot
                'before'

            Set format slot of LiyPond comment::

                >>> note = Note("c'4")
                >>> lilypond_comment = marktools.LilyPondComment('comment')
                >>> lilypond_comment.format_slot = 'after'
                >>> lilypond_comment.format_slot
                'after'

            Set to ``'before'``, ``'after'``, ``'opening'``, ``'closing'``, ``'right'`` or none.
            '''
            return self._format_slot
        def fset(self, format_slot):
            assert format_slot in ('before', 'after', 'opening', 'closing', 'right', None)
            if format_slot is None:
                self._format_slot = 'before'
            else:
                self._format_slot = format_slot
        return property(**locals())
