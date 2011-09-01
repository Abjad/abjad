from abjad.tools.componenttools._Component import _Component
from abjad.tools.marktools.Mark import Mark
import copy


class LilyPondComment(Mark):
    r'''.. versionadded:: 2.0
    
    .. versionchanged:: 2.3
        Changed ``Comment`` to ``LilyPondComment``.

    User-defined comment::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.LilyPondComment('this is a comment')(note)
        LilyPondComment('this is a comment')(c'4)

    ::

        abjad> f(note)
        % this is a comment
        c'4

    Initialize LilyPond comment from contents string; or contents string and format
    slot; or from other LilyPond comment; or from other LilyPond comment and format
    slot.

    LilyPond comments implement ``__slots__``.
    '''

    __slots__ = ('_contents_string', '_format_slot', )

    #def __init__(self, contents_string, format_slot = 'opening'):
    def __init__(self, *args):
        Mark.__init__(self)
        #self._contents_string = contents_string
        #self._format_slot = format_slot
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

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self._contents_string)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._contents_string == arg._contents_string
        return False

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return repr(self._contents_string)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def contents_string():
        def fget(self):
            r'''Get contents string of comment::

                abjad> comment = marktools.LilyPondComment('comment contents string')
                abjad> comment.contents_string
                'comment contents string'

            Set contents string of comment::

                abjad> comment.contents_string = 'new comment contents string'
                abjad> comment.contents_string
                'new comment contents string'

            Set string.
            '''
            return self._contents_string
        def fset(self, contents_string):
            assert isinstance(contents_string, str)
            self._contents_string = contents_string
        return property(**locals())

    @property
    def format(self):
        '''Read-only LilyPond input format of comment:

        ::

            abjad> comment = marktools.LilyPondComment('this is a comment.')
            abjad> comment.format
            '% this is a comment.'

        Return string.
        '''
        from abjad.tools import iotools
        #command = iotools.underscore_delimited_lowercase_to_lowercamelcase(self._contents_string)
        command = iotools.underscore_delimited_lowercase_to_lowercamelcase(self.contents_string)
        return r'%% %s' % command

    @apply
    def format_slot():
        def fget(self):
            '''.. versionadded:: 2.3

            Get format slot of LilyPond comment::
            
                abjad> note = Note("c'4")
                abjad> lilypond_comment = marktools.LilyPondComment('comment')
                abjad> lilypond_comment.format_slot
                'before'

            Set format slot of LiyPond comment::

                abjad> note = Note("c'4")
                abjad> lilypond_comment = marktools.LilyPondComment('comment')
                abjad> lilypond_comment.format_slot = 'after'
                abjad> lilypond_comment.format_slot
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
        return property(**locals( ))
