from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.componenttools.Component import Component


class Mark(AbjadObject):
    '''.. versionadded:: 2.0

    Abstract class from which concrete marks inherit::

        >>> note = Note("c'4")

    ::

        >>> marktools.Mark()(note)
        Mark()(c'4)

    Marks override ``___call__`` to attach to a note, rest or chord.

    Marks are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_start_component', )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 0:
            self._start_component = None
        elif len(args) == 1 and isinstance(args[0], type(self)):
            self._start_component = None
        else:
            raise ValueError('can not initialize mark from {!r}.'.format(args))

    ### SPECIAL METHODS ###

    def __call__(self, *args):
        if len(args) == 0:
            return self.detach()
        elif len(args) == 1:
            return self.attach(args[0])
        else:
            raise ValueError('must call mark with at most 1 argument.')

    def __copy__(self, *args):
        #return type(self)()
        new = type(self)()
        new.format_slot = self.format_slot
        return new

    __deepcopy__ = __copy__

    def __delattr__(self, *args):
        raise AttributeError('can not delete %s attributes.' % type(self).__name__)

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)%s' % (type(self).__name__,
            self._contents_repr_string, self._attachment_repr_string)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _attachment_repr_string(self):
        if self.start_component is None:
            return ''
        else:
            return '(%s)' % str(self.start_component)

    @property
    def _one_line_menuing_summary(self):
        return repr(self)

    ### PRIVATE METHODS ###

    def _bind_start_component(self, start_component):
        #print 'binding MARK to start component ...'
        assert isinstance(start_component, Component)
        self._unbind_start_component()
        start_component._marks_for_which_component_functions_as_start_component.append(self)
        self._start_component = start_component

    def _unbind_start_component(self):
        start_component = self._start_component
        if start_component is not None:
            try:
                start_component._marks_for_which_component_functions_as_start_component.remove(self)
            except ValueError:
                pass
        self._start_component = None

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_component(self):
        '''Read-only reference to mark start component::

            >>> note = Note("c'4")
            >>> mark = marktools.Mark()(note)

        ::

            >>> mark.start_component
            Note("c'4")

        Return component or none.
        '''
        return self._start_component

    ### PUBLIC METHODS ###

    def attach(self, start_component):
        '''Attach mark to `start_component`::

            >>> note = Note("c'4")
            >>> mark = marktools.Mark()

        ::

            >>> mark.attach(note)
            Mark()(c'4)

        ::

            >>> mark.start_component
            Note("c'4")

        Return mark.
        '''
        self._bind_start_component(start_component)
        return self

    def detach(self):
        '''Detach mark::

            >>> note = Note("c'4")
            >>> mark = marktools.Mark()(note)

        ::

            >>> mark.start_component
            Note("c'4")

        ::

            >>> mark.detach()
            Mark()

        ::

            >>> mark.start_component is None
            True

        Return mark.
        '''
        self._unbind_start_component()
        return self
