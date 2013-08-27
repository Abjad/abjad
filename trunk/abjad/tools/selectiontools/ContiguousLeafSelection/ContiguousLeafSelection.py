# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.ContiguousSelection import ContiguousSelection


class ContiguousLeafSelection(ContiguousSelection):
    r'''A selection of time-contiguous leaves.

    ..  container:: example

        **Example.**

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }

        ::

            >>> selection = staff.select_leaves()
            >>> selection
            ContiguousLeafSelection(Note("c'4"), ..., Note("f'4"))
            
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        ContiguousSelection.__init__(self, music=music)
        assert all(isinstance(x, leaftools.Leaf) for x in self)
        assert self._all_are_contiguous_components_in_same_logical_voice(self)

    ### PUBLIC METHODS ###

    def _attach_tie_spanner_to_leaf_pair(self):
        from abjad.tools import leaftools
        from abjad.tools import spannertools
        assert len(self) == 2
        left_leaf, right_leaf = self
        assert isinstance(left_leaf, leaftools.Leaf)
        assert isinstance(right_leaf, leaftools.Leaf)
        left_tie_chain = left_leaf._get_tie_chain()
        right_tie_chain = right_leaf._get_tie_chain()
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

    ### PUBLIC METHODS ###

    def _copy_and_include_enclosing_containers(self):
        from abjad.tools import componenttools
        from abjad.tools import iterationtools
        from abjad.tools import leaftools
        from abjad.tools.mutationtools import mutate
        # get governor
        parentage = self[0]._get_parentage(include_self=True)
        governor = parentage._get_governor()
        # find start and stop indices in governor
        governor_leaves = list(governor.select_leaves())
        for i, x in enumerate(governor_leaves):
            if x is self[0]:
                start_index_in_governor = i
        for i, x in enumerate(governor_leaves):
            if x is self[-1]:
                stop_index_in_governor = i
        # copy governor
        governor_copy = mutate(governor).copy()
        copied_leaves = governor_copy.select_leaves()
        # find start and stop leaves in copy of governor
        start_leaf = copied_leaves[start_index_in_governor]
        stop_leaf = copied_leaves[stop_index_in_governor]
        # trim governor copy forwards from first leaf
        found_start_leaf = False
        while not found_start_leaf:
            leaf = iterationtools.iterate_leaves_in_expr(governor_copy).next()
            if leaf is start_leaf:
                found_start_leaf = True
            else:
                leaftools.remove_leaf_and_shrink_durated_parent_containers(
                    leaf)
        # trim governor copy backwards from last leaf
        found_stop_leaf = False
        while not found_stop_leaf:
            reverse_iterator = iterationtools.iterate_leaves_in_expr(
                governor_copy, reverse=True)
            leaf = reverse_iterator.next()
            if leaf is stop_leaf:
                found_stop_leaf = True
            else:
                leaftools.remove_leaf_and_shrink_durated_parent_containers(
                    leaf)
        # return trimmed governor copy
        return governor_copy

    def detach_grace_containers(self, kind=None):
        r'''Detach grace containers attached to leaves in selection:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> grace_container = leaftools.GraceContainer(
            ...     [Note("cs'16")], 
            ...     kind='grace',
            ...     )
            >>> grace_container(staff[1])
            Note("d'8")

        .. doctest::

            >>> f(staff)
            \new Staff {
                c'8
                \grace {
                    cs'16
                }
                d'8
                e'8
                f'8
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> leaves = staff.select_leaves()
            >>> leaves.detach_grace_containers()
            (GraceContainer(),)

        .. doctest::

            >>> f(staff)
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Return tuple of zero or more grace containers.
        '''
        result = []
        for leaf in self:
            grace_containers = leaf._detach_grace_containers(kind=kind)
            result.extend(grace_containers)
        return tuple(result)

    def replace_with(self, leaf_class):
        r'''Replace leaves in selection with `leaf_class` instances.

        ::

            >>> staff = Staff(2 * Measure((2, 8), "c'8 d'8"))

        .. doctest::

            >>> f(staff)
            \new Staff {
                {
                    \time 2/8
                    c'8
                    d'8
                }
                {
                    c'8
                    d'8
                }
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ..  container:: example

            **Example.** Replace leaves with rests:

            ::

                >>> selection = staff[0].select_leaves()
                >>> selection.replace_with(Rest)

            .. doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 2/8
                        r8
                        r8
                    }
                    {
                        c'8
                        d'8
                    }
                }

            ::

                >>> show(staff) # doctest: +SKIP

        Return none.
        '''
        from abjad.tools import componenttools
        from abjad.tools import leaftools
        from abjad.tools import mutationtools
        assert issubclass(leaf_class, leaftools.Leaf)
        for leaf in self:
            new_leaf = leaf_class(leaf)
            mutationtools.mutate(leaf).replace(new_leaf)
