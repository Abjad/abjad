import types
from abjad.tools.abctools.AbjadObject import AbjadObject


class MinimalSelection(AbjadObject):
    '''Selection of components taken from a single score:

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> selection = staff[:2]
        >>> selection
        Selection(Note("c'4"), Note("d'4"))

    Selection objects will eventually pervade the system and 
    model all user selections.

    This means that selection objects will eventually serve as input
    to most functions in the API. Selection objects will also
    eventually be returned as output from most functions in the API.

    Selections are immutable and never change after instantiation.
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
        #elif isinstance(music, Selection):
        elif isinstance(music, MinimalSelection):
            music = tuple(music)
        elif isinstance(music, types.GeneratorType):
            music = tuple(music)
        else:
            music = (music, )
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        '''Cocatenate `expr` to selection.

        Return new selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = self._music + expr._music
            return type(self)(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = self._music + tuple(expr)
        return type(self)(music)

    def __contains__(self, expr):
        '''True when `expr` is in selection. Otherwise false.

        Return boolean.
        '''
        return expr in self._music

    def __eq__(self, expr):
        '''True when selection and `expr` are of the same type
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
        '''Get item `expr` from selection.

        Return component from selection.
        '''
        result = self._music.__getitem__(expr)
        if isinstance(result, tuple):
            selection = type(self)()
            selection._music = result[:]
            result = selection
        return result

    def __len__(self):
        '''Number of components in selection.

        Return nonnegative integer.
        '''
        return len(self._music)

    def __ne__(self, expr):
        return not self == expr

    def __radd__(self, expr):
        '''Concatenate selection to `expr`.

        Return newly created selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = expr._music + self._music
            #return Selection(music)
            return MinimalSelection(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = tuple(expr) + self._music
        #return Selection(music)
        return MinimalSelection(music)

    def __repr__(self):
        '''Representation of selection in Python interpreter.

        Return string.
        '''
        return '{}{!r}'.format(self._class_name, self._music)

    ### PRIVATE METHODS ###

    def _attach_tie_spanner_to_leaf_pair(self):
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        assert len(self) == 2
        left_leaf, right_leaf = self
        assert isinstance(left_leaf, leaftools.Leaf)
        assert isinstance(right_leaf, leaftools.Leaf)
        left_tie_chain = left_leaf.select_tie_chain()
        right_tie_chain = right_leaf.select_tie_chain()
        spanner_classes = (spannertools.TieSpanner,)
        if left_tie_chain == right_tie_chain:
            return
        try:
            left_tie_spanner = left_leaf._get_spanner(spanner_classes)
        except MissingSpannerError:
            left_tie_spanner = None
        try:
            right_tie_spanner = right_leaf._get_spanner(spanner_classes)
        except MissingSpannerError:
            right_tie_spanner = None
        if left_tie_spanner is not None and right_tie_spanner is not None:
            left_tie_spanner.fuse(right_tie_spanner)
        elif left_tie_spanner is not None and right_tie_spanner is None:
            left_tie_spanner.append(right_leaf)
        elif left_tie_spanner is None and right_tie_spanner is not None:
            right_tie_spanner.append_left(left_leaf)
        elif left_tie_spanner is None and right_tie_spanner is None:
            spannertools.TieSpanner([left_leaf, right_leaf])

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _give_dominant_spanners_to_components(self, recipients):
        '''Find all spanners dominating music.
        Insert each component in recipients into each dominant spanner.
        Remove music from each dominating spanner.
        Return none.
        Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import spannertools
        assert componenttools.all_are_thread_contiguous_components(self)
        assert componenttools.all_are_thread_contiguous_components(recipients)
        receipt = spannertools.get_spanners_that_dominate_components(self)
        for spanner, index in receipt:
            for recipient in reversed(recipients):
                spanner._insert(index, recipient)
            for component in self:
                spanner._remove(component)

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _give_music_to_empty_container(self, container):
        '''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        assert componenttools.all_are_contiguous_components_in_same_parent(
            self)
        assert isinstance(container, containertools.Container)
        assert not container
        music = []
        for component in self:
            music.extend(getattr(component, 'music', ()))
        container._music.extend(music)
        container[:]._set_parents(container)

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _give_position_in_parent_to_container(self, container):
        '''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import containertools
        assert componenttools.all_are_contiguous_components_in_same_parent(
            self)
        assert isinstance(container, containertools.Container)
        parent, start, stop = self.get_parent_and_start_stop_indices()
        if parent is not None:
            parent._music.__setitem__(slice(start, start), [container])
            container._set_parent(parent)
            self._set_parents(None)

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

    def _set_parents(self, new_parent):
        '''Not composer-safe.
        '''
        for component in self._music:
            component._set_parent(new_parent)

    # TODO: eventually migrate method to SliceSelection;
    #       then remove explicit contiguity check.
    def _withdraw_from_crossing_spanners(self):
        '''Not composer-safe.
        '''
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        from abjad.tools import spannertools
        assert componenttools.all_are_thread_contiguous_components(self)
        crossing_spanners = \
            spannertools.get_spanners_that_cross_components(self)
        components_including_children = \
            list(iterationtools.iterate_components_in_expr(self))
        for crossing_spanner in list(crossing_spanners):
            spanner_components = crossing_spanner._components[:]
            for component in components_including_children:
                if component in spanner_components:
                    crossing_spanner._components.remove(component)
                    component._spanners.discard(crossing_spanner)
