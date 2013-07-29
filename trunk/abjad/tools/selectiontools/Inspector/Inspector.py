from abjad.tools.selectiontools.Selection import Selection


class Inspector(Selection):
    '''Selection of components grouped together for inspection.
    '''

    ### PUBLIC METHODS ###

    def get_badly_formed_components(self):
        r'''Get badly formed components in selection:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> staff[1].written_duration = Duration(1, 4)
            >>> spannertools.BeamSpanner(staff[:])
            BeamSpanner(c'8, d'4, e'8, f'8)

        ::

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

        Return list.
        '''
        from abjad.tools import wellformednesstools
        badly_formed_components = []
        for checker in wellformednesstools.Check.list_checks():
            badly_formed_components.extend(checker.violators(self))
        return badly_formed_components

    @staticmethod
    def inspect(expr):
        from abjad.tools import componenttools
        if isinstance(expr, componenttools.Component):
            return Inspector(expr)
        elif hasattr(expr, '_music'):
            music = expr._music
            return Inspector(music)
        else:
            return Inspector(expr)

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

    def tabulate_well_formedness_violations(self):
        r'''Tabulate well-formedness violations in selection:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> staff[1].written_duration = Duration(1, 4)
            >>> spannertools.BeamSpanner(staff[:])
            BeamSpanner(c'8, d'4, e'8, f'8)

        ::

            >>> f(staff)
            \new Staff {
                c'8 [
                d'4
                e'8
                f'8 ]
            }

        ::

            >>> result =  inspect(staff).tabulate_well_formedness_violations()

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
