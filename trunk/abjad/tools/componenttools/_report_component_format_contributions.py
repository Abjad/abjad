from abjad.components._Component import _Component
from abjad.tools.spannertools import Spanner


def _report_component_format_contributions(component, verbose = False, output = 'screen'):
   r'''Read-only string report of all format-time contributions
   made to `component` by all the different parts of the Abjad
   system plumbing.

   Set `verbose` to True or False.
   
   Set `output` to 'screen' or 'string'.
   '''

   if isinstance(component, _Component): 
      return component._formatter.report(verbose = verbose, output = output)
   elif isinstance(component, Spanner):
      return component._format.report(output = output)
   else:
      raise TypeError('neither component nor spanner: "%s".' % component)
