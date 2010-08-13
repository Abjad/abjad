from abjad.core import Rational
from abjad.tools import listtools
from abjad.tools import mathtools


## TODO: Maybe move get_likely_multiplier_of_components( ) from durtools to measuretools? ##

def get_likely_multiplier_of_components(components):
   r'''Get likely multiplier of arbitrary `components`. ::

      abjad> staff = Staff(macros.scale(4, (7, 32)))
      abjad> f(staff)
      \new Staff {
         c'8..
         d'8..
         e'8..
         f'8..
      }
      abjad> componenttools.get_likely_multiplier_of_components(staff[:])
      Rational(7, 4)
   
   Return ``1`` on no likely multiplier. ::

      abjad> staff = Staff(macros.scale(4))
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
      }
      abjad> componenttools.get_likely_multiplier_of_components(staff[:])
      Rational(1, 1)

   Return none on more than one likely multiplier. ::

      abjad> staff = Staff(notetools.make_notes([0, 2, 4, 5], [(3, 16), (7, 32)]))
      abjad> f(staff)
      \new Staff {
         c'8.
         d'8..
         e'8.
         f'8..
      }
      abjad> componenttools.get_likely_multiplier_of_components(staff[:]) is None
      True

   Function implemented to help reverse measure subsumption.
   
   .. todo:: move to ``durtools``?

   .. versionchanged:: 1.1.2
      renamed ``componenttools.get_likely_multiplier( )`` to
      ``componenttools.get_likely_multiplier_of_components( )``.
   '''
   from abjad.tools import componenttools
   from abjad.tools import tietools

   assert componenttools.all_are_components(components)

   chain_duration_numerators = [ ]
   for expr in tietools.iterate_topmost_tie_chains_and_components_forward_in_expr(components):
      if tietools.is_tie_chain(expr):
         chain_duration = tietools.get_preprolated_tie_chain_duration(expr)   
         chain_duration_numerators.append(chain_duration.numerator)
       
   if len(listtools.unique(chain_duration_numerators)) == 1:
      numerator = chain_duration_numerators[0]
      denominator = mathtools.greatest_power_of_two_less_equal(numerator)
      likely_multiplier = Rational(numerator, denominator)
      return likely_multiplier
