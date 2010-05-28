from abjad.rational import Rational
from abjad.tools import check
from abjad.tools import iterate
from abjad.tools import listtools
from abjad.tools import mathtools


## TODO: Maybe move get_likely_multiplier( ) from durtools to measuretools? ##

def get_likely_multiplier(components):
   r'''Get likely multiplier of arbitrary `components`. ::

      abjad> staff = Staff(construct.scale(4, (7, 32)))
      abjad> f(staff)
      \new Staff {
         c'8..
         d'8..
         e'8..
         f'8..
      }
      abjad> componenttools.get_likely_multiplier(staff[:])
      Rational(7, 4)
   
   Return ``1`` on no likely multiplier. ::

      abjad> staff = Staff(construct.scale(4))
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
      }
      abjad> componenttools.get_likely_multiplier(staff[:])
      Rational(1, 1)

   Return none on more than one likely multiplier. ::

      abjad> staff = Staff(construct.notes([0, 2, 4, 5], [(3, 16), (7, 32)]))
      abjad> f(staff)
      \new Staff {
         c'8.
         d'8..
         e'8.
         f'8..
      }
      abjad> componenttools.get_likely_multiplier(staff[:]) is None
      True

   Function implemented to help reverse measure subsumption.
   
   .. todo:: move to ``durtools``?
   '''

   from abjad.tools import tietools
   check.assert_components(components)

   chain_duration_numerators = [ ]
   for expr in iterate.chained_contents(components):
      if tietools.is_chain(expr):
         chain_duration = tietools.get_duration_preprolated(expr)   
         chain_duration_numerators.append(chain_duration._n)
       
   if len(listtools.unique(chain_duration_numerators)) == 1:
      numerator = chain_duration_numerators[0]
      denominator = mathtools.greatest_power_of_two_less_equal(numerator)
      likely_multiplier = Rational(numerator, denominator)
      return likely_multiplier
