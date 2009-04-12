from abjad.exceptions.exceptions import ParallelError
from abjad.tools.check.are_contexts import are_contexts


def assert_are_contexts(expr):
   if not are_contexts(expr):
      raise ParallelError('Parallel containers must contain Contexts only.') 
