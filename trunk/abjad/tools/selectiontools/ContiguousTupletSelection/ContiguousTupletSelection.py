# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.ContiguousSelection import ContiguousSelection


class ContiguousTupletSelection(ContiguousSelection):
    '''A selection of time-contiguous tuplets.
    '''

    ### PUBLIC METHODS ###

    def fuse(self):
        r'''Fuse parent-contiguous tuplets in selection.

        ..  container:: example
        
            **Example.** Fuse parent-contiguous fxed-duration tuplets
            in selection:

            ::

                >>> t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), [])
                >>> t1.extend("c'8 d'8 e'8")
                >>> beam = spannertools.BeamSpanner(t1[:])
                >>> t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), [])
                >>> t2.extend("c'16 d'16 e'16")
                >>> slur = spannertools.SlurSpanner(t2[:])
                >>> staff = Staff([t1, t2])

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8 [
                        d'8
                        e'8 ]
                    }
                    \times 2/3 {
                        c'16 (
                        d'16
                        e'16 )
                    }
                }

            ::

                >>> show(staff) # doctest: +SKIP

            ::

                >>> tuplets = selectiontools.select_tuplets(staff[:],
                ...     recurse=False)
                >>> tuplets.fuse()
                FixedDurationTuplet(3/8, [c'8, d'8, e'8, c'16, d'16, e'16])

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \times 2/3 {
                        c'8 [
                        d'8
                        e'8 ]
                        c'16 (
                        d'16
                        e'16 )
                    }
                }

            ::

                >>> show(staff) # doctest: +SKIP

        Return new tuplet.

        Fuse zero or more parent-contiguous `tuplets`.

        Allow in-score `tuplets`.

        Allow outside-of-score `tuplets`.

        All `tuplets` must carry the same multiplier.

        All `tuplets` must be of the same type.
        '''
        from abjad.tools import containertools
        from abjad.tools import tuplettools
        assert self._all_are_contiguous_components_in_same_parent(
            component_classes=(tuplettools.Tuplet,))
        if len(self) == 0:
            return None
        first = self[0]
        first_multiplier = first.multiplier
        first_type = type(first)
        for tuplet in self[1:]:
            if tuplet.multiplier != first_multiplier:
                raise TupletFuseError('tuplets must carry same multiplier.')
            if type(tuplet) != first_type:
                raise TupletFuseError('tuplets must be same type.')
        if isinstance(first, tuplettools.FixedDurationTuplet):
            total_contents_duration = sum(
                [x._contents_duration for x in self])
            new_target_duration = first_multiplier * total_contents_duration
            new_tuplet = tuplettools.FixedDurationTuplet(
                new_target_duration, [])
        elif isinstance(first, tuplettools.Tuplet):
            new_tuplet = tuplettools.Tuplet(first_multiplier, [])
        else:
            raise TypeError('unknown tuplet type.')
        wrapped = False
        if self[0]._select_parentage().root is not \
            self[-1]._select_parentage().root:
            dummy_container = containertools.Container(self)
            wrapped = True
        containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
            self, new_tuplet)
        if wrapped:
            del(dummy_container[:])
        return new_tuplet
