from .. core.interface import _Interface

class DynamicsInterface(_Interface):
   
   def __init__(self, client):
      self._client = client
      self._mark = None

   @property
   def _summary(self):
      result = [ ]
      if self.mark:
         result.append(self.mark)
      if self.hairpin:
         result.append(self.hairpin)
      if result:
         return ', '.join([str(x) for x in result])
      else:
         return ' '

   def __repr__(self):
      return 'DynamicsInterface(%s)' % self._summary

   @property
   def hairpins(self):
      return self._client.spanners.get(classname = '_Hairpin')

   @property
   def hairpin(self):
      if self.hairpins:
         return self.hairpins[0]
      else:
         return None

   @apply
   def mark( ):
      def fget(self):
         return self._mark
      def fset(self, arg):
         if arg is None:
            self._mark = arg
         elif isinstance(arg, str):
            self._mark = arg
         else:
            raise ValueError('dynamics %s must be str or None.' % str(arg))
      return property(**locals( ))

   @property
   def effective(self):
      if self.hairpin:
         return self.hairpin
      else:
         if self.mark:
            return self.mark
         else:
            cur = self._client.prev
            while cur:
               if cur.dynamics.hairpin:
                  return cur.dynamics.hairpin.stop
               elif cur.dynamics.mark:
                  return cur.dynamics.mark
               else:
                  cur = cur.prev
            return None

   ### FORMATTING ###

   @property
   def _right(self):
      result = [ ]
      if self.mark:
         result.append(r'\%sX' % self.mark)
      return result
