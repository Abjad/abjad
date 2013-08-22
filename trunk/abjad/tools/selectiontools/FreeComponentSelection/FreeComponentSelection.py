# -*- encoding: utf-8 -*-
import copy
from abjad.tools.selectiontools.Selection import Selection


class FreeComponentSelection(Selection):
    r'''A selection of components grouped together for inspection.
    '''

    ### PUBLIC METHODS ###

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

    def report_modifications(self):
        r'''Report modifications of components in selection.

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
