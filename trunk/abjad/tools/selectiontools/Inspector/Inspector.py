# -*- encoding: utf-8 -*-
from abjad.tools.selectiontools.Selection import Selection


class Inspector(Selection):
    r'''Access to extended component methods.
    '''

    ### PUBLIC METHODS ###

    def detach_grace_containers(self, kind=None):
        r'''Detaches grace containers attached to component.

        Returns tuple.
        '''
        return self[0]._detach_grace_containers(
            kind=kind,
            )

    def get_annotation_value(self, name, default=None):
        r'''Gets value of annotation with `name` attached to component.

        Returns `default` when no annotation with `name` is attached
        to component.

        Raises exception when more than one annotation with `name`
        is attached to component.
        '''
        from abjad.tools import marktools
        annotations = self.get_marks(marktools.Annotation)
        if not annotations:
            return default
        with_correct_name = []
        for annotation in annotations:
            if annotation.name == name:
                with_correct_name.append(annotation)
        if not with_correct_name:
            return default
        if 1 < len(with_correct_name):
            raise Exception('more than one annotation.')
        annotation_value = with_correct_name[0].value
        return annotation_value

    def get_duration(self, in_seconds=False):
        r'''Gets duration of component.

        Returns duration.
        '''
        return self[0]._get_duration(
            in_seconds=in_seconds,
            )

    def get_effective_context_mark(
        self,
        context_mark_classes=None,
        ):
        r'''Gets effective context mark of `context_mark_class` 
        that governs component.

        Returns context mark or none.
        '''
        return self[0]._get_effective_context_mark(
            context_mark_classes=context_mark_classes,
            )

    def get_effective_staff(self):
        r'''Gets effective staff of component.

        Returns staff or none.
        '''
        return self[0]._get_effective_staff()

    def get_grace_containers(self, kind=None):
        r'''Gets grace containers attached to leaf.

        ..  container:: example

            **Example 1.** Get all grace containers attached to note:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> grace_container = leaftools.GraceContainer(
                ...     [Note("cs'16")], 
                ...     kind='grace',
                ...     )
                >>> grace_container.attach(staff[1])
                Note("d'8")
                >>> after_grace = leaftools.GraceContainer(
                ...     [Note("ds'16")], 
                ...     kind='after'
                ...     )
                >>> after_grace.attach(staff[1])
                Note("d'8")
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8
                    \grace {
                        cs'16
                    }
                    \afterGrace
                    d'8
                    {
                        ds'16
                    }
                    e'8
                    f'8
                }

            ::

                >>> more(staff[1]).get_grace_containers()
                (GraceContainer(cs'16), GraceContainer(ds'16))

        ..  container:: example

            **Example 2.** Get only (proper) grace containers attached to note:

            ::

                >>> more(staff[1]).get_grace_containers(kind='grace')
                (GraceContainer(cs'16),)

        ..  container:: example

            **Example 3.** Get only after grace containers attached to note:

            ::

                >>> more(staff[1]).get_grace_containers(kind='after')
                (GraceContainer(ds'16),)

        Set `kind` to ``'grace'``, ``'after'`` or none.

        Returns tuple.
        '''
        return self[0]._get_grace_containers(
            kind=kind,
            )

    def get_mark(
        self,
        mark_classes=None,
        ):
        r'''Gets exactly one mark of `mark_classes` attached to component.

        Raises exception when no mark of `mark_classes` is attached
        to component.

        Returns mark.
        '''
        return self[0]._get_mark(
            mark_classes=mark_classes,
            )

    def get_marks(
        self,
        mark_classes=None,
        ):
        r'''Get all marks of `mark_classes` attached to component.

        Return tuple.
        '''
        return self[0]._get_marks(
            mark_classes=mark_classes,
            )

    def get_markup(
        self,
        direction=None,
        ):
        r'''Gets all markup attached to component.

        Returns tuple.
        '''
        return self[0]._get_markup(
            direction=direction,
            )

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of component.

        Returns timespan.
        '''
        return self[0]._get_timespan(
            in_seconds=in_seconds,
            )

    def get_spanners(self):
        r'''Gets spanners attached to component.

        Returns set.
        '''
        return self[0]._get_spanners()


    def select_components(self, component_classes=None, include_self=True):
        r'''Selects all components of `component_classes`
        in the descendants of component.

        Returns component selection.
        '''
        return self[0]._select_components(
            component_classes=component_classes,
            include_self=include_self,
            )

    def select_contents(self, include_self=True):
        r'''Selects contents of component.

        Returns sequential selection.
        '''
        return self[0]._select_contents(
            include_self=include_self,
            )

    # TODO: remove cross_offset keyword
    def select_descendants(
        self,
        cross_offset=None,
        include_self=True,
        ):
        r'''Selects descendants of component.

        Returns descendants.
        '''
        return self[0]._select_descendants(
            cross_offset=cross_offset,
            include_self=include_self,
            )

    def select_lineage(self):
        r'''Selects lineage of component.
        
        Returns lineage.
        '''
        return self[0]._select_lineage()

    def select_parentage(self, include_self=True):
        r'''Selects parentage of component.

        Returns parentage.
        '''
        return self[0]._select_parentage(
            include_self=include_self,
            )

    def select_tie_chain(self):
        r'''Selects tie chain that governs leaf.

        Returns tie chain.
        '''
        return self[0]._select_tie_chain()

    def select_vertical_moment(self, governor=None):
        r'''Selects vertical moment starting with component.

        Returns vertical moment.
        '''
        return self[0]._select_vertical_moment(
            governor=governor,
            )

    def select_vertical_moment_at(self, offset):
        r'''Selects vertical moment at `offset`.

        Returns vertical moment.
        '''
        return self[0]._select_vertical_moment_at(
            offset,
            )
