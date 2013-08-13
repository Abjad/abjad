# -*- encoding: utf-8 -*-
import copy
import types


class Selection(object):
    r'''A selection of components.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_music',
        )

    _default_positional_input_arguments = (
        [],
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        if music is None:
            music = ()
        elif isinstance(music, (tuple, list)):
            music = tuple(music)
        elif isinstance(music, Selection):
            music = tuple(music)
        elif isinstance(music, types.GeneratorType):
            music = tuple(music)
        else:
            music = (music, )
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Cocatenate `expr` to selection.

        Return new selection.
        '''
        assert isinstance(expr, (Selection, list, tuple))
        if isinstance(expr, Selection):
            music = self._music + expr._music
            return type(self)(music)
        elif isinstance(expr, (tuple, list)):
            music = self._music + tuple(expr)
        return type(self)(music)

    def __contains__(self, expr):
        r'''True when `expr` is in selection. Otherwise false.

        Return boolean.
        '''
        return expr in self._music

    def __eq__(self, expr):
        r'''True when selection and `expr` are of the same type
        and when music of selection equals music of `expr`.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            return self._music == expr._music
        # eventually remove this permissive branch
        # and force the use of selections only
        elif isinstance(expr, (list, tuple)):
            return self._music == tuple(expr)

    def __getitem__(self, expr):
        r'''Get item `expr` from selection.

        Return component from selection.
        '''
        result = self._music.__getitem__(expr)
        if isinstance(result, tuple):
            selection = type(self)()
            selection._music = result[:]
            result = selection
        return result

    def __len__(self):
        r'''Number of components in selection.

        Return nonnegative integer.
        '''
        return len(self._music)

    def __ne__(self, expr):
        r'''True when selection does not equal `expr`. Otherwise false.

        Return boolean.
        '''
        return not self == expr

    def __radd__(self, expr):
        r'''Concatenate selection to `expr`.

        Return newly created selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = expr._music + self._music
            return Selection(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = tuple(expr) + self._music
        return Selection(music)

    def __repr__(self):
        r'''Selection interpreter representation.

        Return string.
        '''
        return '{}{!r}'.format(self.__class__.__name__, self._music)

    ### PRIVATE METHODS ###

    def _all_are_components(self, component_classes=None):
        from abjad.tools import componenttools
        return componenttools.all_are_components(
            self,
            component_classes=component_classes,
            )

    def _all_are_components_in_same_logical_voice(
        self, classes=None, allow_orphans=True):
        from abjad.tools import componenttools
        return componenttool.all_are_components_in_same_logical_voice(
            classes=classes,
            allow_orphans=allow_orphans,
            )
    
    def _all_are_contiguous_components(
        self, component_classes=None, allow_orphans=True):
        from abjad.tools import componenttools
        return componenttools.all_are_contiguous_components(
            self,
            component_classes=component_classes,
            allow_orphans=allow_orphans,
            )

    def _all_are_contiguous_components_in_same_parent(
        self, component_classes=None, allow_orphans=True):
        from abjad.tools import componenttools
        return componenttools.all_are_contiguous_components_in_same_parent(
            self,
            component_classes=component_classes,
            allow_orphans=allow_orphans,
            )

    def _all_are_logical_voice_contiguous_components(
        self, component_classes=None, allow_orphans=True):
        from abjad.tools import componenttools
        return componenttools.all_are_logical_voice_contiguous_components(
            self,
            component_classes=component_classes,
            allow_orphans=allow_orphans,
            )

    def _attach_marks(self, marks, recurse=False):
        from abjad.tools import marktools
        if not isinstance(marks, (list, tuple)):
            marks = (marks,)
        instantiated_marks = []
        for mark in marks:
            if not isinstance(mark, marktools.Mark):
                if issubclass(mark, marktools.Mark):
                    mark = mark()
            assert isinstance(mark, marktools.Mark)
            instantiated_marks.append(mark)
        marks = instantiated_marks
        result = []
        for component in self._iterate_components(recurse=recurse):
            for mark in marks:
                copied_mark = copy.copy(mark)
                copied_mark.attach(component)
                result.append(copied_mark)
        return tuple(result)

    def _attach_spanners(self, spanner, recurse=False):
        from abjad.tools import spannertools
        if issubclass(spanner, spannertools.Spanner):
            spanner = spanner()
        assert isinstance(spanner, spannertools.Spanner)
        spanners = []
        for component in self._iterate_components(recurse=recurse):
            copied_spanner = copy.copy(spanner)
            copied_spanner.attach([component])
            spanners.append(copied_spanner)
        return tuple(spanners)

    def _detach_marks(self, mark_classes=None, recurse=True):
        marks = []
        for component in self._iterate_components(recurse=recurse):
            marks.extend(component._detach_marks(mark_classes=mark_classes))
        return tuple(marks)

    def _detach_spanners(self, spanner_classes=None, recurse=True):
        spanners = []
        for component in self._iterate_components(recurse=recurse):
            spanners.extend(
                component._detach_spanners(spanner_classes=spanner_classes))
        return tuple(spanners)

    def _get_component(self, component_classes=None, n=0, recurse=True):
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        component_classes = component_classes or (componenttools.Component,)
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes,)
        if 0 <= n:
            if recurse:
                components = iterationtools.iterate_components_in_expr(
                    self, component_classes)
            else:
                components = self._music
            for i, x in enumerate(components):
                if i == n:
                    return x
        else:
            if recurse:
                components = iterationtools.iterate_components_in_expr(
                    self, component_classes, reverse=True)
            else:
                components = reversed(self._music)
            for i, x in enumerate(components):
                if i == abs(n) - 1:
                    return x

    def _get_marks(self, mark_classes=None, recurse=True):
        result = []
        for component in self._iterate_components(recurse=recurse):
            marks = component._get_marks(mark_classes=mark_classes)
            result.extend(marks)
        return tuple(result)

    def _iterate_components(self, recurse=True, reverse=False):
        from abjad.tools import iterationtools
        if recurse:
            return iterationtools.iterate_components_in_expr(self)
        else:
            return self._iterate_top_level_components(reverse=reverse)

    def _iterate_top_level_components(self, reverse=False):
        if reverse:
            for component in reversed(self):
                yield component
        else:
            for component in self:
                yield component
