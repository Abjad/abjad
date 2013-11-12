# -*- encoding: utf-8 -*-
import types
from abjad.tools.topleveltools import iterate


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
        music = self._coerce_music(music)
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Cocatenates `expr` to selection.

        Returns new selection.
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

        Returns boolean.
        '''
        return expr in self._music

    def __eq__(self, expr):
        r'''True when selection and `expr` are of the same type
        and when music of selection equals music of `expr`.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self._music == expr._music
        elif isinstance(expr, (list, tuple)):
            return self._music == tuple(expr)

    def __getitem__(self, expr):
        r'''Gets item `expr` from selection.

        Returns component from selection.
        '''
        result = self._music.__getitem__(expr)
        if isinstance(result, tuple):
            selection = type(self)()
            selection._music = result[:]
            result = selection
        return result

    def __len__(self):
        r'''Number of components in selection.

        Returns nonnegative integer.
        '''
        return len(self._music)

    def __ne__(self, expr):
        r'''True when selection does not equal `expr`. Otherwise false.

        Returns boolean.
        '''
        return not self == expr

    def __radd__(self, expr):
        r'''Concatenates selection to `expr`.

        Returns newly created selection.
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
        r'''Interpreter representation of selection.

        Returns string.
        '''
        return '{}{!r}'.format(type(self).__name__, self._music)

    ### PRIVATE PROPERTIES ###

    @property
    def _preprolated_duration(self):
        return sum(component._preprolated_duration for component in self)

    @property
    def _tools_package_qualified_repr(self):
        return 'selectiontools.{}({!r})'.format(
            type(self).__name__, list(self))

    ### PRIVATE METHODS ###

    @staticmethod
    def _all_are_components_in_same_logical_voice(
        expr, component_classes=None, allow_orphans=True):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        allowable_types = (
            list,
            tuple,
            types.GeneratorType,
            selectiontools.Selection,
            )
        if not isinstance(expr, allowable_types):
            return False
        component_classes = component_classes or (scoretools.Component,)
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes, )
        assert isinstance(component_classes, tuple)
        if len(expr) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in expr:
                if not isinstance(component, component_classes):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = expr[0]
        if not isinstance(first, component_classes):
            return False
        orphan_components = True
        if not first._get_parentage().is_orphan:
            orphan_components = False
        same_logical_voice = True
        first_signature = first._get_parentage().logical_voice_indicator
        for component in expr[1:]:
            parentage = component._get_parentage()
            if not parentage.is_orphan:
                orphan_components = False
            if not allow_orphans and orphan_components:
                return False
            if parentage.logical_voice_indicator != first_signature:
                same_logical_voice = False
            if not allow_orphans and not same_logical_voice:
                return False
            if allow_orphans and not orphan_components and \
                not same_logical_voice:
                return False
        return True
    
    @staticmethod
    def _all_are_contiguous_components_in_same_logical_voice(
        expr, component_classes=None, allow_orphans=True):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        allowable_types = (
            list,
            tuple,
            types.GeneratorType,
            selectiontools.Selection,
            )
        if not isinstance(expr, allowable_types):
            return False
        component_classes = component_classes or (scoretools.Component,)
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes, )
        assert isinstance(component_classes, tuple)
        if len(expr) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in expr:
                if not isinstance(component, component_classes):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        if not allow_orphans:
            if any(x._get_parentage().is_orphan for x in expr):
                return False
        first = expr[0]
        if not isinstance(first, component_classes):
            return False
        first_parentage = first._get_parentage()
        first_logical_voice_indicator = first_parentage.logical_voice_indicator
        first_root = first_parentage.root
        previous = first
        for current in expr[1:]:
            current_parentage = current._get_parentage()
            current_logical_voice_indicator = \
                current_parentage.logical_voice_indicator
            # false if wrong type of component found
            if not isinstance(current, component_classes):
                return False
            # false if in different logical voices
            if current_logical_voice_indicator != first_logical_voice_indicator:
                return False
            # false if components are in same score and are discontiguous
            if current_parentage.root == first_root:
                if not previous._is_immediate_temporal_successor_of(current):
                    return False
            previous = current
        return True

    @staticmethod
    def _all_are_contiguous_components_in_same_parent(
        expr, component_classes=None, allow_orphans=True):
        from abjad.tools import scoretools
        from abjad.tools import selectiontools
        allowable_types = (
            list,
            tuple,
            types.GeneratorType,
            selectiontools.Selection,
            )
        if not isinstance(expr, allowable_types):
            return False
        component_classes = component_classes or (scoretools.Component, )
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes, )
        assert isinstance(component_classes, tuple)
        if len(expr) == 0:
            return True
        all_are_orphans_of_correct_type = True
        if allow_orphans:
            for component in expr:
                if not isinstance(component, component_classes):
                    all_are_orphans_of_correct_type = False
                    break
                if not component._get_parentage().is_orphan:
                    all_are_orphans_of_correct_type = False
                    break
            if all_are_orphans_of_correct_type:
                return True
        first = expr[0]
        if not isinstance(first, component_classes):
            return False
        first_parent = first._parent
        if first_parent is None:
            if allow_orphans:
                orphan_components = True
            else:
                return False
        same_parent = True
        strictly_contiguous = True
        previous = first
        for current in expr[1:]:
            if not isinstance(current, component_classes):
                return False
            if not current._get_parentage().is_orphan:
                orphan_components = False
            if not current._parent is first_parent:
                same_parent = False
            if not previous._is_immediate_temporal_successor_of(current):
                strictly_contiguous = False
            if (not allow_orphans or 
                (allow_orphans and not orphan_components)) and \
                (not same_parent or not strictly_contiguous):
                return False
            previous = current
        return True

    @staticmethod
    def _coerce_music(music):
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
        return music

    def _get_component(self, component_classes=None, n=0, recurse=True):
        from abjad.tools import scoretools
        component_classes = component_classes or (scoretools.Component,)
        if not isinstance(component_classes, tuple):
            component_classes = (component_classes,)
        if 0 <= n:
            if recurse:
                components = iterate(self).by_class(component_classes)
            else:
                components = self._music
            for i, x in enumerate(components):
                if i == n:
                    return x
        else:
            if recurse:
                components = iterate(self).by_class(
                    component_classes, reverse=True)
            else:
                components = reversed(self._music)
            for i, x in enumerate(components):
                if i == abs(n) - 1:
                    return x

    def _get_spanner(self, spanner_classes=None):
        spanners = self._get_spanners(spanner_classes=spanner_classes)
        if not spanners:
            message = 'no spanners found.'
            raise MissingSpannerError(message)
        elif len(spanners) == 1:
            return spanners.pop()
        else:
            message = 'multiple spanners found.'
            raise ExtraSpannerError(message)

    def _get_spanners(self, spanner_classes=None):
        from abjad.tools import spannertools
        spanner_classes = spanner_classes or (spannertools.Spanner,)
        if not isinstance(spanner_classes, tuple):
            spanner_classes = (spanner_classes, )
        assert isinstance(spanner_classes, tuple)
        result = set()
        for component in self:
            spanners = component._get_spanners(spanner_classes)
            result.update(spanners)
        return result

    def _iterate_components(self, recurse=True, reverse=False):
        if recurse:
            return iterate(self).by_class()
        else:
            return self._iterate_top_level_components(reverse=reverse)

    def _iterate_top_level_components(self, reverse=False):
        if reverse:
            for component in reversed(self):
                yield component
        else:
            for component in self:
                yield component

    def _set_parents(self, new_parent):
        r'''Not composer-safe.
        '''
        for component in self._music:
            component._set_parent(new_parent)

    ### PUBLIC METHODS ###

    def get_duration(self, in_seconds=False):
        r'''Gets duration of contiguous selection.

        Returns duration.
        '''
        return sum(
            component._get_duration(in_seconds=in_seconds) 
            for component in self
            )

    def get_spanners(self, spanner_classes=None):
        r'''Gets spanners attached to any component in selection.

        Returns set.
        '''
        result = set()
        for component in self:
            spanners = component._get_spanners(spanner_classes=spanner_classes)
            result.update(spanners)
        return result
