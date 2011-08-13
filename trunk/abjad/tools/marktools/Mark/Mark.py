from abjad.tools.componenttools._Component import _Component


class Mark(object):
    '''.. versionadded:: 2.0

    Abstract class from which concrete marks inherit::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.Mark( )(note)
        Mark( )(c'4)

    Marks override ``___call__`` to attach to a note, rest or chord.

    Marks implement ``__slots__``.
    '''

    __slots__ = ('_start_component', )

    def __init__(self):
        self._start_component = None

    ### OVERLOADS ###

    def __call__(self, *args):
        if len(args) == 0:
            return self.detach_mark( )
        elif len(args) == 1:
            return self.attach_mark(args[0])
        else:
            raise ValueError('must call mark with at most 1 argument.')

    def __copy__(self, *args):
        return type(self)( )

    __deepcopy__ = __copy__

    def __delattr__(self, *args):
        raise AttributeError('can not delete %s attributes.' % self.__class__.__name__)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)%s' % (self.__class__.__name__,
            self._contents_repr_string, self._attachment_repr_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _attachment_repr_string(self):
        if self.start_component is None:
            return ''
        else:
            return '(%s)' % str(self.start_component)

    @property
    def _contents_repr_string(self):
        if hasattr(self, 'contents'):
            return repr(self.contents)
        else:
            return ' '

    ### MANGLED METHODS ###

    ### method must NOT be preceeded by __ so that child ContextMark objects can call it
    def _bind_start_component(self, start_component):
        #print 'binding MARK to start component ...'
        assert isinstance(start_component, _Component)
        self.__unbind_start_component( )
        start_component._marks_for_which_component_functions_as_start_component.append(self)
        self._start_component = start_component

    def __unbind_start_component(self):
        start_component = self._start_component
        if start_component is not None:
            try:
                start_component._marks_for_which_component_functions_as_start_component.remove(self)
            except ValueError:
                pass
        self._start_component = None

    ### PUBLIC ATTRIBUTES ###

    @property
    def start_component(self):
        '''Read-only reference to mark start component::

            abjad> note = Note("c'4")
            abjad> mark = marktools.Mark( )(note)

        ::

            abjad> mark.start_component
            Note("c'4")

        Return component or none.
        '''
        return self._start_component

    ### PUBLIC METHODS ###

    def attach_mark(self, start_component):
        '''Attach mark to `start_component`::

            abjad> note = Note("c'4")
            abjad> mark = marktools.Mark( )

        ::

            abjad> mark.attach_mark(note)
            Mark( )(c'4)

        ::

            abjad> mark.start_component
            Note("c'4")

        Return mark.
        '''
        self._bind_start_component(start_component)
        return self

    def detach_mark(self):
        '''Detach mark::

            abjad> note = Note("c'4")
            abjad> mark = marktools.Mark( )(note)

        ::

            abjad> mark.start_component
            Note("c'4")

        ::

            abjad> mark.detach_mark( )
            Mark( )

        ::

            abjad> mark.start_component is None
            True

        Return mark.
        '''
        self.__unbind_start_component( )
        return self

