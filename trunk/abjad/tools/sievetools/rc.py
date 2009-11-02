from abjad.tools.sievetools.baserc import _BaseRC
from abjad.tools.sievetools.process_min_max_attribute import _process_min_max_attribute

class RC(_BaseRC):
   '''Residue class (or congruence class). 
   Use to construct sieves a la Xenakis.'''

   def __init__(self, modulo, residue):
      if not modulo > 0:
         raise ValueError('modulo must be > 0.')
      if not 0 <= residue < modulo:
         raise ValueError('abs(residue) must be < modulo')

      self.modulo = modulo # period
      self.residue = residue # phase


   def get_congruent_bases(self, *min_max):
      '''Returns all the congruent bases of this residue class within the 
      given range. 
      The method takes one or two integer arguments. If only one it given, 
      it is taken as the *max* range and *min* is assumed to be 0.
      
      Example::
         
         abjad> r = RC(3, 0)
         abjad> r.get_congruent_bases(6)
         [0, 3, 6]
         abjad> r.get_congruent_bases(-6, 6)
         [-6, -3, 0, 3, 6] '''

      min, max = _process_min_max_attribute(*min_max)
      result = [ ]
      for i in range(min, max + 1): 
         if i % self.modulo == self.residue:
            result.append(i)
      return result
         

   def get_boolean_train(self, *min_max):
      '''Returns a boolean train with 0s mapped to the integers
      that are not congruent bases of the residue class and 1s mapped
      to those that are.
      The method takes one or two integer arguments. If only one it given, 
      it is taken as the *max* range and *min* is assumed to be 0.

      Example::

         abjad> r = RC(3, 0) 
         abjad> r.get_boolean_train(6)
         [1, 0, 0, 1, 0, 0]
         abjad> k.get_congruent_bases(-6, 6)
         [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]'''

      min, max = _process_min_max_attribute(*min_max)
      result = [ ]
      for i in range(min, max):
         if i % self.modulo == self.residue:
            result.append(1)
         else:
            result.append(0)
      return result


   ## OVERRIDES ##

   def __eq__(self, exp):
      if isinstance(exp, RC):
         return (self.modulo == exp.modulo) and (self.residue == exp.residue)
      else:
         return False


   def __repr__(self):
      return 'RC(%i, %i)' % (self.modulo, self.residue)




if __name__ == '__main__':
   
   print 'Psappha B2[0:40]'
   s1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
   s2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
   s3 = RC(8, 3) #&  RC(1, 0)
   s4 = RC(8, 4) #&  RC(1, 0)
   s5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
   s6 = (RC(8, 1) & RC(5, 2))
   s7 = (RC(8, 6) & RC(5, 1))

   y = s1 | s2 | s3 | s4 | s5 | s6 | s7 
   print y
   print 'congruent bases:\n', y.get_congruent_bases(40)
   print 'boolen train:\n', y.get_boolean_train(40)
