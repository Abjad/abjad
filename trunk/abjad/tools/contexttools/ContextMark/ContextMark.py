from abjad.exceptions import ExtraMarkError
from abjad.tools.contexttools._Context import _Context
from abjad.tools.marktools.Mark import Mark


class ContextMark(Mark):
    '''.. versionadded:: 2.0

    Abstract class from which concrete context marks inherit::

        abjad> note = Note("c'4")

    ::

        abjad> contexttools.ContextMark()(note)
        ContextMark()(c'4)

    Context marks override ``__call__`` to attach to Abjad components.

    Context marks implement ``__slots__``.
    '''

    __slots__ = ('_effective_context', '_target_context', )

    def __init__(self, target_context = None):
        Mark.__init__(self)
        self._effective_context = None
        if target_context is not None:
            if not isinstance(target_context, type):
                raise TypeError('target context "%s" must be context class.' % target_context)
        self._target_context = target_context

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(target_context = self._target_context)

    __deepcopy__ = __copy__

    ### MANGLED METHODS ###

    def __bind_correct_effective_context(self, correct_effective_context):
        self.__unbind_effective_context()
        if correct_effective_context is not None:
            correct_effective_context._marks_for_which_component_functions_as_effective_context.append(
                self)
        self._effective_context = correct_effective_context
        correct_effective_context._mark_entire_score_tree_for_later_update('marks')

    def __unbind_effective_context(self):
        effective_context = self._effective_context
        if effective_context is not None:
            try:
                effective_context._marks_for_which_component_functions_as_effective_context.remove(self)
            except ValueError:
                pass
        self._effective_context = None

    def _bind_start_component(self, start_component):
        #print 'binding CONTEXT MARK to start component ...'
        Mark._bind_start_component(self, start_component)
        self._start_component._mark_entire_score_tree_for_later_update('marks')

    ### PRIVATE ATTRIBUTES ###

    @property
    def _target_context_name(self):
        if isinstance(self._target_context, type):
            return self._target_context.__name__
        else:
            return type(self._target_context).__name__

    ### PRIVATE METHODS ###

    def _find_correct_effective_context(self):
        from abjad.tools import componenttools
        target_context = self.target_context
        if target_context is None:
            return None
        elif isinstance(target_context, type):
            target_context_type = target_context
            for component in componenttools.get_improper_parentage_of_component(self.start_component):
                if isinstance(component, target_context_type):
                    return component
        elif isinstance(target_context, str):
            target_context_name = target_context
            for component in componenttools.get_improper_parentage_of_component(self.start_component):
                if component.name == target_context_name:
                    return component
        else:
            raise TypeError('target context "%s" must be context type, context name or none.' %
                target_context)

    def _update_effective_context(self):
        '''This function is designed to be called by score components during score update.
        '''
        #print '\tupdating effective context of %s ...' % type(self).__name__
        current_effective_context = self._effective_context
        correct_effective_context = self._find_correct_effective_context()
        if current_effective_context is not correct_effective_context:
            self.__bind_correct_effective_context(correct_effective_context)

    ### PUBLIC ATTRIBUTES ###

    @property
    def effective_context(self):
        '''Read-only reference to effective context of context mark:

        ::

            abjad> note = Note("c'4")
            abjad> context_mark = contexttools.ContextMark()(note)

        ::

            abjad> context_mark.effective_context is None
            True

        Return context mark or none.
        '''
        if self.start_component is not None:
            self.start_component._update_marks_of_entire_score_tree_if_necessary()
        return self._effective_context

    @property
    def target_context(self):
        '''Read-only reference to target context of context mark:

        ::

            abjad> note = Note("c'4")
            abjad> context_mark = contexttools.ContextMark()(note)

        ::

            abjad> context_mark.target_context is None
            True

        Return context mark or none.
        '''
        return self._target_context

    ### PUBLIC METHODS ###

    def attach(self, start_component):
        '''Make sure no context mark of same type is already attached to start component.
        '''
        from abjad.tools import contexttools
        klasses = (type(self), )
        if contexttools.is_component_with_context_mark_attached(start_component, klasses):
            raise ExtraMarkError('component already has context mark attached.')
        return Mark.attach(self, start_component)

    def detach(self):
        '''Detach mark:

        ::

            abjad> note = Note("c'4")
            abjad> context_mark = contexttools.ContextMark()(note)

        ::

            abjad> context_mark.start_component
            Note("c'4")

        ::

            abjad> context_mark.detach()
            ContextMark()

        ::

            abjad> context_mark.start_component is None
            True

        Return context mark.
        '''
        Mark.detach(self)
        self.__unbind_effective_context()
        return self
