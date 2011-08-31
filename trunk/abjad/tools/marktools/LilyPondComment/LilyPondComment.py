from abjad.tools.componenttools._Component import _Component
from abjad.tools.marktools.Mark import Mark


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

    LilyPond comments implement ``__slots__``.
    '''

    __slots__ = ('_comment_name', '_format_slot', )

    def __init__(self, comment_name, format_slot = 'opening'):
        Mark.__init__(self)
        self._comment_name = comment_name
        self._format_slot = format_slot

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self._comment_name)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._comment_name == arg._comment_name
        return False

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return repr(self._comment_name)

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
            return self._comment_name
        def fset(self, contents_string):
            assert isinstance(contents_string, str)
            self._comment_name = contents_string
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
        command = iotools.underscore_delimited_lowercase_to_lowercamelcase(self._comment_name)
        return r'%% %s' % command

