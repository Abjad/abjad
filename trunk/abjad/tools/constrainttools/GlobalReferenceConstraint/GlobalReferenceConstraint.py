from abjad.tools.constrainttools._GlobalConstraint._GlobalConstraint import _GlobalConstraint


class GlobalReferenceConstraint(_GlobalConstraint):
    r'''A global constraint with an arbitrary external reference:

    ::

        abjad> from abjad.tools.constrainttools import GlobalReferenceConstraint
    
    Its predicate function should accept two arguments, the first being the
    current solution, and the second for the external reference provided at
    instantiation.

    ::

        abjad> reference = [0, 1, 2, 3]
        abjad> predicate = lambda solution, reference: all([item not in reference for item in solution])
        abjad> constraint = GlobalReferenceConstraint(reference, predicate)

    ::

        abjad> constraint([-1, 10, 3.5])
        True
        abjad> constraint([-1, 1, 2, 3, 23])
        False
        
    ``GlobalReferenceConstraints`` are immutable.    

    Returns ``GlobalReferenceConstraint`` instance.
    '''

    __slots__ = ('_kind', '_predicate', '_reference')

    def __init__(self, reference, predicate):
        object.__setattr__(self, '_kind', 'global')
        object.__setattr__(self, '_reference', reference)
        assert isinstance(predicate, type(lambda: None))
        assert predicate.func_code.co_argcount == 2
        object.__setattr__(self, '_predicate', predicate)

    ### OVERRIDES ###

    def __call__(self, solution):
        return self._predicate(solution, self._reference)

    ### PUBLIC PROPERTIES ###

    @property
    def reference(self):
        return self._reference
