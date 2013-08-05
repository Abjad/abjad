# -*- encoding: utf-8 -*-
import copy
from abjad.tools.selectiontools.FreeSelection import FreeSelection


class ComponentSelection(FreeSelection):
    r'''Selection of components grouped together for inspection.
    '''

    ### PUBLIC METHODS ###

    def attach_marks(self, marks, recurse=False):
        r'''Attach copy of each mark in `marks` 
        to each component in selection.

        Return tuple of marks created.
        '''
        return self._attach_marks(marks, recurse=recurse)

    def attach_spanners(self, spanner, recurse=False):
        r'''Attach shallow copy of `spanner` 
        to each component in selection.

        Return list of spanners created.
        '''
        return self._attach_spanners(spanner, recurse=recurse)
        
    def detach_marks(self, mark_classes=None, recurse=True):
        return self._detach_marks(mark_classes=mark_classes, recurse=recurse)

    def detach_spanners(self, spanner_classes=None, recurse=True):
        r'''Detach `spanner_classes` from components in selection.

        Example 1. Detach tie spanners from components in selection:

        ::

            >>> staff = Staff("e'4 ( ~ e'16 fs'8 ~ fs'16 )")
            >>> time_signature = contexttools.TimeSignatureMark((2, 4))
            >>> time_signature.attach(staff)
            TimeSignatureMark((2, 4))(Staff{4})

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 2/4
                e'4 ( ~
                e'16
                fs'8 ~
                fs'16 )
            }

        ::

            >>> show(staff) # doctest: +SKIP

        ::

            >>> select(staff).detach_spanners(
            ...     spanner_classes=(spannertools.TieSpanner,))
            (TieSpanner(), TieSpanner())

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \time 2/4
                e'4 (
                e'16
                fs'8
                fs'16 )
            }

        ::

            >>> show(staff) # doctest: +SKIP

        Detach spanners from components at all levels
        of selection when `recurse` is true.

        Detach spanners at only top level of selection
        when `recurse` is false.

        Detach all spanners when `spanner_classes` is none.

        Detach spanners of only `spanner_classes` when
        `spanners_classes` is not none.

        Return none.
        '''
        return self._detach_spanners(
            spanner_classes=spanner_classes, 
            recurse=recurse,
            )

    def get_badly_formed_components(self):
        r'''Get badly formed components in selection:

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

            >>> select(staff).get_badly_formed_components()
            [Note("d'4")]

        (Beamed quarter notes are not well formed.)

        Return list.
        '''
        from abjad.tools import wellformednesstools
        badly_formed_components = []
        for checker in wellformednesstools.Check.list_checks():
            badly_formed_components.extend(checker.violators(self))
        return badly_formed_components

    def get_component(self, component_classes=None, n=0, recurse=True):
        r'''Get component `n` of `component_classes` in selection.

        Iterate only top level when `recurse` is false.

        Iterate depth-first when `recurse` is true.

        Return component or none.
        '''
        return self._get_component(
            component_classes=component_classes,
            n=n,
            recurse=recurse,
            )

    def get_marks(self, mark_classes=None, recurse=True):
        r'''Get `mark_classes` attached to components in selection.

        Return tuple.
        '''
        return self._get_marks(mark_classes=mark_classes, recurse=recurse)

    def is_well_formed(self, allow_empty_containers=True):
        from abjad.tools import wellformednesstools
        results = []
        for component in self:
            for checker in wellformednesstools.Check.list_checks():
                if allow_empty_containers:
                    if getattr(checker, 'runtime', False) == 'composition':
                        continue
                results.append(checker.check(component))
        return all(results)

    def report_modifications(self):
        r'''Report modifications of components in selection.

        Example. Report modifications of container in selection:

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

            >>> selection = select(container)
            >>> report = selection.report_modifications()

        ::

            >>> print report
            {
                \override NoteHead #'color = #red
                \override NoteHead #'style = #'harmonic
                %%% 4 components omitted %%%
                \revert NoteHead #'color
                \revert NoteHead #'style
            }

        Return string.
        '''
        from abjad.tools import containertools
        from abjad.tools import formattools
        for component in self:
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
        r'''Tabulate well-formedness violations in selection:

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

            >>> result =  select(staff).tabulate_well_formedness_violations()

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
        '''
        from abjad.tools import wellformednesstools
        lines = []
        for checker in wellformednesstools.Check.list_checks():
            lines.append(checker.report(self))
        result = '\n'.join(lines)
        return result
