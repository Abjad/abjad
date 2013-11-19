# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextMark(AbjadObject):
    '''A context mark.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_effective_context',
        '_scope',
        '_start_component',
        )

    ### INITIALIZER ###

    def __init__(self):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff
        self._effective_context = None
        self._scope = None
        self._start_component = None

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

#    def __repr__(self):
#        r'''Interpreter representation of context mark.
#
#        Returns string.
#        '''
#        return '{}({}){}'.format(
#            type(self).__name__,
#            self._contents_repr_string,
#            self._attachment_repr_string,
#            )

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
    def _scope_name(self):
        if isinstance(self.scope, type):
            return self.scope.__name__
        else:
            return type(self.scope).__name__

    ### PRIVATE METHODS ###

    def _attach(self, start_component):
        r'''Attaches context mark to `start_component`.

        Makes sure no context mark of same type is already attached
        to score component that starts with start component.

        Returns context mark.
        '''
        from abjad.tools import indicatortools
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
        self._bind_to_start_component(start_component)

    def _bind_correct_effective_context(self, correct_effective_context):
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_context_marks.append(
                self)
        self._effective_context = correct_effective_context
        self._update_effective_context()

    def _bind_to_start_component(self, start_component):
        from abjad.tools import scoretools
        assert isinstance(start_component, scoretools.Component)
        self._unbind_start_component()
        start_component._start_context_marks.append(self)
        self._start_component = start_component
        self._update_effective_context()

    def _detach(self):
        self._unbind_start_component()
        self._unbind_effective_context()
        return self

    def _find_correct_effective_context(self):
        from abjad.tools import scoretools
        scope = self.scope
        if scope is None:
            return None
        elif isinstance(scope, type):
            scope_type = scope
            for component in self._start_component._get_parentage():
                if isinstance(component, scope_type):
                    return component
        elif isinstance(scope, str):
            scope_name = scope
            for component in self._start_component._get_parentage():
                if component.name == scope_name:
                    return component
        else:
            message = 'target context {!r} must be'
            message += ' context type, context name or none.'
            message = message.format(scope)
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
                start_component._start_context_marks.remove(self)
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

    ### PUBLIC PROPERTIES ###

    @property
    def scope(self):
        return self._scope or self._default_scope
