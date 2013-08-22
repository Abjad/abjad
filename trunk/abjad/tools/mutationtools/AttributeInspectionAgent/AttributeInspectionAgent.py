# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class AttributeInspectionAgent(AbjadObject):
    r'''Inspect one component.
    '''

    ### INITIALIZER ###

    def __init__(self, component):
        from abjad.tools import componenttools
        assert isinstance(component, componenttools.Component)
        self._component = component

    ### PUBLIC METHODS ###

    def detach_grace_containers(self, kind=None):
        r'''Detaches grace containers attached to component.

        Returns tuple.
        '''
        return self._component._detach_grace_containers(
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

    def get_badly_formed_components(self):
        r'''Gets badly formed components in component.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> staff[1].written_duration = Duration(1, 4)
                >>> spannertools.BeamSpanner(staff[:])
                BeamSpanner(c'8, d'4, e'8, f'8)

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> inspect(staff).get_badly_formed_components()
                [Note("d'4")]

            (Beamed quarter notes are not well formed.)

        Returns list.
        '''
        from abjad.tools import wellformednesstools
        badly_formed_components = []
        for checker in wellformednesstools.Check.list_checks():
            badly_formed_components.extend(checker.violators(self._component))
        return badly_formed_components

    def get_duration(self, in_seconds=False):
        r'''Gets duration of component.

        Returns duration.
        '''
        return self._component._get_duration(
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
        return self._component._get_effective_context_mark(
            context_mark_classes=context_mark_classes,
            )

    def get_effective_staff(self):
        r'''Gets effective staff of component.

        Returns staff or none.
        '''
        return self._component._get_effective_staff()

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

                >>> inspect(staff[1]).get_grace_containers()
                (GraceContainer(cs'16), GraceContainer(ds'16))

        ..  container:: example

            **Example 2.** Get only (proper) grace containers attached to note:

            ::

                >>> inspect(staff[1]).get_grace_containers(kind='grace')
                (GraceContainer(cs'16),)

        ..  container:: example

            **Example 3.** Get only after grace containers attached to note:

            ::

                >>> inspect(staff[1]).get_grace_containers(kind='after')
                (GraceContainer(ds'16),)

        Set `kind` to ``'grace'``, ``'after'`` or none.

        Returns tuple.
        '''
        return self._component._get_grace_containers(
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
        return self._component._get_mark(
            mark_classes=mark_classes,
            )

    def get_marks(
        self,
        mark_classes=None,
        ):
        r'''Get all marks of `mark_classes` attached to component.

        Returns tuple.
        '''
        return self._component._get_marks(
            mark_classes=mark_classes,
            )

    def get_markup(
        self,
        direction=None,
        ):
        r'''Gets all markup attached to component.

        Returns tuple.
        '''
        return self._component._get_markup(
            direction=direction,
            )

    def get_timespan(self, in_seconds=False):
        r'''Gets timespan of component.

        Returns timespan.
        '''
        return self._component._get_timespan(
            in_seconds=in_seconds,
            )

    def get_spanners(self):
        r'''Gets spanners attached to component.

        Returns set.
        '''
        return self._component._get_spanners()

    def is_bar_line_crossing(self):
        r'''True when component crosses bar line.
        Otherwise false.

        ..  container:: example

            **Example.**

            ::

                >>> staff = Staff("c'4 d'4 e'4")
                >>> time_signature = contexttools.TimeSignatureMark((3, 8))
                >>> time_signature.attach(staff)
                TimeSignatureMark((3, 8))(Staff{3})
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    \time 3/8
                    c'4
                    d'4
                    e'4
                }

            ::

                >>> for note in staff:
                ...     result = inspect(note).is_bar_line_crossing()
                ...     print '{}\t{}'.format(note, result)
                c'4 False
                d'4 True
                e'4 False

        Returns boolean.
        '''
        from abjad.tools import contexttools
        time_signature = self._component._get_effective_context_mark(
            contexttools.TimeSignatureMark)
        if time_signature is None:
            time_signature_duration = durationtools.Duration(4, 4)
        else:
            time_signature_duration = time_signature.duration
        partial = getattr(time_signature, 'partial', 0)
        partial = partial or 0
        start_offset = self._component._get_timespan().start_offset
        shifted_start = start_offset - partial
        shifted_start %= time_signature_duration
        stop_offset = self._component._get_duration() + shifted_start
        if time_signature_duration < stop_offset:
            return True
        return False

    def get_components(self, component_classes=None, include_self=True):
        r'''Gets all components of `component_classes`
        in the descendants of component.

        Returns component selection.
        '''
        return self._component._get_components(
            component_classes=component_classes,
            include_self=include_self,
            )

    def get_contents(self, include_self=True):
        r'''Gets contents of component.

        Returns sequential selection.
        '''
        return self._component._get_contents(
            include_self=include_self,
            )

    def get_descendants(
        self,
        include_self=True,
        ):
        r'''Gets descendants of component.

        Returns descendants.
        '''
        return self._component._get_descendants(
            include_self=include_self,
            )

    def get_lineage(self):
        r'''Gets lineage of component.
        
        Returns lineage.
        '''
        return self._component._get_lineage()

    def get_parentage(self, include_self=True):
        r'''Gets parentage of component.

        Returns parentage.
        '''
        return self._component._get_parentage(
            include_self=include_self,
            )

    def get_tie_chain(self):
        r'''Gets tie chain that governs leaf.

        Returns tie chain.
        '''
        return self._component._get_tie_chain()

    def get_vertical_moment(self, governor=None):
        r'''Gets vertical moment starting with component.

        Returns vertical moment.
        '''
        return self._component._get_vertical_moment(
            governor=governor,
            )

    def get_vertical_moment_at(self, offset):
        r'''Gets vertical moment at `offset`.

        Returns vertical moment.
        '''
        return self._component._get_vertical_moment_at(
            offset,
            )

    def is_well_formed(self, allow_empty_containers=True):
        r'''True when component is well-formed.
        Otherwise false.

        Returns false.
        '''
        from abjad.tools import wellformednesstools
        results = []
        for checker in wellformednesstools.Check.list_checks():
            if allow_empty_containers:
                if getattr(checker, 'runtime', False) == 'composition':
                    continue
            results.append(checker.check(self._component))
        return all(results)

    def report_modifications(self):
        r'''Reports modifications of component.

        ..  container:: example

            **Example.** Report modifications of container in selection:

            ::

                >>> container = Container("c'8 d'8 e'8 f'8")
                >>> container.override.note_head.color = 'red'
                >>> container.override.note_head.style = 'harmonic'
                >>> show(container) # doctest: +SKIP

            ..  doctest::

                >>> f(container)
                {
                    \override NoteHead #'color = #red
                    \override NoteHead #'style = #'harmonic
                    c'8
                    d'8
                    e'8
                    f'8
                    \revert NoteHead #'color
                    \revert NoteHead #'style
                }

            ::

                >>> report = inspect(container).report_modifications()

            ::

                >>> print report
                {
                    \override NoteHead #'color = #red
                    \override NoteHead #'style = #'harmonic
                    %%% 4 components omitted %%%
                    \revert NoteHead #'color
                    \revert NoteHead #'style
                }

        Returns string.
        '''
        from abjad.tools import containertools
        from abjad.tools import formattools
        component = self._component
        format_contributions = formattools.get_all_format_contributions(
            component)
        result = []
        result.extend(component._get_format_contributions_for_slot(
            'before', format_contributions))
        result.extend(component._get_format_contributions_for_slot(
            'open brackets', format_contributions))
        result.extend(component._get_format_contributions_for_slot(
            'opening', format_contributions))
        result.append('\t%%%%%% %s components omitted %%%%%%' % len(component))
        result.extend(component._get_format_contributions_for_slot(
            'closing', format_contributions))
        result.extend(component._get_format_contributions_for_slot(
            'close brackets', format_contributions))
        result.extend(component._get_format_contributions_for_slot(
            'after', format_contributions))
        result = '\n'.join(result)
        return result

    def tabulate_well_formedness_violations(self):
        r'''Tabulates well-formedness violations in component.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> staff[1].written_duration = Duration(1, 4)
                >>> spannertools.BeamSpanner(staff[:])
                BeamSpanner(c'8, d'4, e'8, f'8)

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    c'8 [
                    d'4
                    e'8
                    f'8 ]
                }

            ::

                >>> result = inspect(staff).tabulate_well_formedness_violations()

            ::

                >>> print result
                1 /    4 beamed quarter note
                0 /    1 discontiguous spanner
                0 /    5 duplicate id
                0 /    1 empty container
                0 /    0 intermarked hairpin
                0 /    0 misdurated measure
                0 /    0 misfilled measure
                0 /    4 mispitched tie
                0 /    4 misrepresented flag
                0 /    5 missing parent
                0 /    0 nested measure
                0 /    1 overlapping beam
                0 /    0 overlapping glissando
                0 /    0 overlapping octavation
                0 /    0 short hairpin

            Beamed quarter notes are not well formed.

        Returns string.
        '''
        from abjad.tools import wellformednesstools
        lines = []
        for checker in wellformednesstools.Check.list_checks():
            lines.append(checker.report(self._component))
        result = '\n'.join(lines)
        return result


def inspect(component):
    r'''Inspect `component`.

    Returns inspector.
    '''
    return AttributeInspectionAgent(component)
