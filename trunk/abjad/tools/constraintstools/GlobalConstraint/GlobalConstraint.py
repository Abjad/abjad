from abjad.tools.constraintstools._Constraint._Constraint import _Constraint


class GlobalConstraint(_Constraint):
    r'''A constraint applied against an entire solution:

    ::

        abjad> from abjad.tools.constraintstools import GlobalConstraint

    Instantiated from a function which takes a single argument, representing an
    entire solution.

    ::

        abjad> max_total_range = GlobalConstraint(lambda seq: (max(seq) - min(seq)) < 5)

    ::

        abjad> max_total_range([0, 1, 2])
        True
        abjad> max_total_range([0, 1, 2, 3])
        True
        abjad> max_total_range([0, 1, 2, 3, 4])
        True
        abjad> max_total_range([0, 1, 2, 3, 4, 5])
        False

    ``GlobalConstraints`` are immutable.

    Returns ``GlobalConstraint`` instance.
    '''

    __slots__ = ('procedure')

    def __init__(self, procedure):
        assert isinstance(procedure, type(lambda: None))
        assert procedure.func_code.co_argcount == 1
        object.__setattr__(self, 'procedure', procedure)

    ### OVERRIDES ###

    def __call__(self, solution):
        return self.procedure(solution)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return '%r' % self.procedure
