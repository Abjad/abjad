# -*- encoding: utf-8 -*-
#from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.marktools.Mark import Mark


#class ContextMark(AbjadObject):
class ContextMark(Mark):
    '''A context mark.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_effective_context', 
        '_start_component',
        '_target_context',
        )

    ### INITIALIZER ###

    def __init__(self):
        from abjad.tools import scoretools
        self._effective_context = None
        self._start_component = None
        self._target_context = scoretools.Staff

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies context mark.

        Returns new context mark.
        '''
        return type(self)()

    def __format__(self, format_specification=''):
        r'''Formats context mark.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __repr__(self):
        r'''Interpreter representation of context mark.

        Returns string.
        '''
        return '{}({}){}'.format(
            type(self).__name__,
            self._contents_repr_string, 
            self._attachment_repr_string,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _attachment_repr_string(self):
        if self._start_component is None:
            return ''
        else:
            return '({!s})'.format(self._start_component)

    @property
    def _one_line_menuing_summary(self):
        return repr(self)

    @property
    def _target_context_name(self):
        if isinstance(self._target_context, type):
            return self._target_context.__name__
        else:
            return type(self._target_context).__name__

    ### PRIVATE METHODS ###

    def _attach(self, start_component):
        r'''Attaches context mark to `start_component`.
        
        Makes sure no context mark of same type is already attached 
        to score component that starts with start component.

        Returns context mark.
        '''
        from abjad.tools import marktools
        classes = (type(self), )
        effective_context_mark = \
            start_component._get_effective_context_mark(classes)
        if effective_context_mark is not None:
            timespan = effective_context_mark._start_component._get_timespan()
            mark_start_offset = timespan.start_offset
            timespan = start_component._get_timespan()
            start_component_start_offset = timespan.start_offset
            if mark_start_offset == start_component_start_offset:
                message = 'effective context mark already attached'
                message += ' to component starting at same time.'
                raise ValueError(message)
        #return Mark._attach(self, start_component)
        self._bind_to_start_component(start_component)

    def _bind_correct_effective_context(self, correct_effective_context):
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_context_marks.append(
                self)
        self._effective_context = correct_effective_context
        self._update_effective_context()

    def _bind_to_start_component(self, start_component):
        #Mark._bind_to_start_component(self, start_component)
        from abjad.tools import scoretools
        assert isinstance(start_component, scoretools.Component)
        self._unbind_start_component()
        start_component._start_marks.append(self)
        self._start_component = start_component
        self._update_effective_context()

    def _detach(self):
        #Mark._detach(self)
        self._unbind_start_component()
        self._unbind_effective_context()
        return self

    def _find_correct_effective_context(self):
        from abjad.tools import scoretools
        target_context = self._target_context
        if target_context is None:
            return None
        elif isinstance(target_context, type):
            target_context_type = target_context
            for component in self._start_component._get_parentage():
                if isinstance(component, target_context_type):
                    return component
        elif isinstance(target_context, str):
            target_context_name = target_context
            for component in self._start_component._get_parentage():
                if component.name == target_context_name:
                    return component
        else:
            message = 'target context {!r} must be'
            message += ' context type, context name or none.'
            message = message.format(target_context)
            raise TypeError(message)

    def _get_effective_context(self):
        if self._start_component is not None:
            self._start_component._update_now(marks=True)
        return self._effective_context

    def _unbind_effective_context(self):
        effective_context = self._effective_context
        if effective_context is not None:
            try:
                effective_context._dependent_context_marks.remove(self)
            except ValueError:
                pass
        self._effective_context = None

    def _unbind_start_component(self):
        start_component = self._start_component
        if start_component is not None:
            try:
                start_component._start_marks.remove(self)
            except ValueError:
                pass
        self._start_component = None

    def _update_effective_context(self):
        r'''This function is designed to be called by score components 
        during score update.
        '''
        current_effective_context = self._effective_context
        correct_effective_context = self._find_correct_effective_context()
        if current_effective_context is not correct_effective_context:
            self._bind_correct_effective_context(correct_effective_context)
