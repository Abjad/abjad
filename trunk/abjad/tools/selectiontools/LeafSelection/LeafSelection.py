from abjad.tools.selectiontools.HorizontalSelection import HorizontalSelection


class LeafSelection(HorizontalSelection):
    '''Selection of leaves.
    '''

    ### INITIALIZER ###

    def __init__(self, music=None):
        from abjad.tools import leaftools
        HorizontalSelection.__init__(self, music=music)
        assert all(isinstance(x, leaftools.Leaf) for x in self)

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

        ..  lilypond

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

        ..  lilypond

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
