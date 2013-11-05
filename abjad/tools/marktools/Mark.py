# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Mark(AbjadObject):
    r'''A mark.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_component',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 0:
            self._start_component = None
        elif len(args) == 1 and isinstance(args[0], type(self)):
            self._start_component = None
        else:
            message = 'can not initialize mark from {!r}.'
            message = message.format(args)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies mark.
            
        Returns new mark.
        '''
        new = type(self)()
        new.format_slot = self.format_slot
        return new

    def __eq__(self, expr):
        r'''True when `expr` is the same type as self.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return True
        return False

    def __format__(self, format_specification=''):
        r'''Gets format.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        r'''Interpreter representation of mark.

        Returns string.
        '''
        return '{}({}){}'.format(
            self._class_name,
            self._contents_repr_string, 
            self._attachment_repr_string,
            )

    ### PRIVATE PROPERTIES ###

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
        from abjad.tools import scoretools
        #print 'binding MARK to start component ...'
        assert isinstance(start_component, scoretools.Component)
        self._unbind_start_component()
        start_component._start_marks.append(self)
        self._start_component = start_component

    def _unbind_start_component(self):
        start_component = self._start_component
        if start_component is not None:
            try:
                start_component._start_marks.remove(self)
            except ValueError:
                pass
        self._start_component = None

    ### PUBLIC PROPERTIES ###

    @property
    def start_component(self):
        r'''Start component of mark.

        Returns component or none.
        '''
        return self._start_component

    @property
    def storage_format(self):
        r'''Storage format of mark.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr

    ### PUBLIC METHODS ###

    def _attach(self, start_component):
        r'''Attaches mark to `start_component`.

        Returns mark.
        '''
        self._bind_start_component(start_component)
        return self

    def detach(self):
        r'''Detaches mark from start component.

        Returns mark.
        '''
        self._unbind_start_component()
        return self
