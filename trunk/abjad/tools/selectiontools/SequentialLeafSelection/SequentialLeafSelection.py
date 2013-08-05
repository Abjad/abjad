# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.SliceSelection import SliceSelection


class SequentialLeafSelection(SliceSelection):
    r'''SliceSelection of leaves.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        from abjad.tools import leaftools
        SliceSelection.__init__(self, music=music)
        assert all(isinstance(x, leaftools.Leaf) for x in self)

    ### PUBLIC METHODS ###

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

    ### PUBLIC METHODS ###

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
            grace_containers = leaf.detach_grace_containers(kind=kind)
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
        assert issubclass(leaf_class, leaftools.Leaf)
        for leaf in self:
            new_leaf = leaf_class(leaf)
            componenttools.move_parentage_and_spanners_from_components_to_components(
                [leaf], [new_leaf])
