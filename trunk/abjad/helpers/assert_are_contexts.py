from abjad.exceptions.exceptions import ParallelError
from abjad.helpers.assess_are_contexts import assess_are_contexts

def assert_are_contexts(expr):
   if not assess_are_contexts(expr):
      raise ParallelError('Parallel containers must contain Contexts only.') 
