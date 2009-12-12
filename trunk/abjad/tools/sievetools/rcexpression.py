from abjad.tools.sievetools.baserc import _BaseRC
from abjad.tools.sievetools.process_min_max_attribute import \
   _process_min_max_attribute
import operator


class RCexpression(_BaseRC):

   def __init__(self, rcs, operator = 'or'):
      self.rcs = rcs[:]
      self.operator = operator
      self._sort_rcs( )

   ## OVERLOADS ##

   def __repr__(self):
      opdic = {'and':' & ', 'or':' | ', 'xor':' ^ '}
      result = opdic[self.operator].join([str(rc) for rc in self.rcs])
      return '{%s}' % result

   ## PRIVATE METHODS ##

   def _get_congruent_bases(self, min, max, op):
      if op is operator.iand:
         result = set(range(min, max + 1))
      else:
         result = set([ ])
      for rc in self.rcs:
         op(result, set(rc.get_congruent_bases(min, max)))
      return sorted(result)

   def _sort_rcs(self): 
      from abjad.tools.sievetools.rc import RC
      if all([isinstance(rc, RC) for rc in self.rcs]):
         self.rcs.sort( )

   ## PUBLIC METHODS ##

   def get_boolean_train(self, *min_max):
      '''Returns a boolean train with 0s mapped to the integers
      that are not congruent bases of the RC expression and 1s mapped
      to those that are.
      The method takes one or two integer arguments. 
      If only one is given, it is taken as the max range 
      and min is assumed to be 0.

      Example::

         abjad> e = RC(3, 0) | RC(2, 0)
         abjad> e.get_boolean_train(6)
         [1, 0, 1, 1, 1, 0]
         abjad> e.get_congruent_bases(-6, 6)
         [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
      '''

      min, max = _process_min_max_attribute(*min_max)
      result = [ ] 
      cb = self.get_congruent_bases(min, max)
      for i in range(min, max ):
         if i in cb:
            result.append(1)
         else:
            result.append(0)
      return result

   def get_congruent_bases(self, *min_max):
      '''Returns all the congruent bases of this RC expression 
      within the given range. 
      The method takes one or two integer arguments. 
      If only one it given, it is taken as the max range 
      and min is assumed to be 0.
      
      Example::
         
         abjad> e = RC(3, 0) | RC(2, 0)
         abjad> e.get_congruent_bases(6)
         [0, 2, 3, 4, 6]
         abjad> e.get_congruent_bases(-6, 6)
         [-6, -4, -3, -2, 0, 2, 3, 4, 6]
      '''

      min, max = _process_min_max_attribute(*min_max)
      if self.operator == 'or':
         return self._get_congruent_bases(min, max, operator.ior)
      elif self.operator == 'xor':
         return self._get_congruent_bases(min, max, operator.ixor)
      elif self.operator == 'and':
         return self._get_congruent_bases(min, max, operator.iand)
