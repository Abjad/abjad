import copy
from abjad.tools.selectiontools.FreeSelection import FreeSelection


class ComponentSelection(FreeSelection):
    '''Selection of components grouped together for inspection.
    '''

    ### PUBLIC METHODS ###

    def attach_marks(self, marks, recurse=False):
        '''Attach copy of each mark in `marks` 
        to each component in selection.

        Return tuple of marks created.
        '''
        from abjad.tools import marktools
        if not isinstance(marks, (list, tuple)):
            marks = (marks,)
        instantiated_marks = []
        for mark in marks:
            if not isinstance(mark, marktools.Mark):
                if issubclass(mark, marktools.Mark):
                    mark = mark()
            assert isinstance(mark, marktools.Mark)
            instantiated_marks.append(mark)
        marks = instantiated_marks
        result = []
        for component in self._iterate_components(recurse=recurse):
            for mark in marks:
                copied_mark = copy.copy(mark)
                copied_mark.attach(component)
                result.append(copied_mark)
        return tuple(result)
        
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

    def get_marks(self, mark_classes=None, recurse=True):
        '''Get `mark_classes` attached to components in selection.

        Return tuple.
        '''
        return self._get_marks(mark_classes=mark_classes, recurse=recurse)

    @staticmethod
    def inspect(expr):
        from abjad.tools import componenttools
        if isinstance(expr, componenttools.Component):
            return ComponentSelection(expr)
        elif hasattr(expr, '_music'):
            music = expr._music
            return ComponentSelection(music)
        else:
            return ComponentSelection(expr)

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
