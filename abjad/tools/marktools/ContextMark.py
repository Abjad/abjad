# -*- encoding: utf-8 -*-
from abjad.tools.marktools.Mark import Mark


class ContextMark(Mark):
    '''Abstract class from which concrete context marks inherit.

    Context marks are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_effective_context', 
        '_target_context',
        )

    ### INITIALIZER ###

    def __init__(self, _target_context=None):
        Mark.__init__(self)
        self._effective_context = None
        if _target_context is not None:
            if not isinstance(_target_context, type):
                message = 'target context {!r} must be context class.'
                message = message.format(_target_context)
                raise TypeError(message)
        self._target_context = _target_context

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies context mark.

        Returns new context mark.
        '''
        return type(self)(_target_context=self._target_context)

    def __format__(self, format_specification=''):
        r'''Formats context mark.

        Set `format_specification` to `''`, `'lilypond`' or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        superclass = super(ContextMark, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE PROPERTIES ###

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
                raise ExtraMarkError(message)
        return Mark._attach(self, start_component)

    def _bind_correct_effective_context(self, correct_effective_context):
        self._unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._dependent_context_marks.append(
                self)
        self._effective_context = correct_effective_context
        self._update_effective_context()

    def _bind_start_component(self, start_component):
        Mark._bind_start_component(self, start_component)
        self._update_effective_context()

    def _detach(self):
        Mark._detach(self)
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

    def _unbind_effective_context(self):
        effective_context = self._effective_context
        if effective_context is not None:
            try:
                effective_context._dependent_context_marks.remove(self)
            except ValueError:
                pass
        self._effective_context = None

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
    def effective_context(self):
        r'''Effective context of context mark.

        Returns context mark or none.
        '''
        if self._start_component is not None:
            self._start_component._update_now(marks=True)
        return self._effective_context
