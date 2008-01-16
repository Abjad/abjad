class Invocation(object):

   def __init__(self, client, lhs = None, rhs = None, modifications = [ ]):
      self._client = client
      self.lhs = lhs
      self.rhs = rhs
      self.modifications = [ ]
      self.modifications.extend(modifications)

   ### REPR ###

   def __repr__(self):
      result = [ ]
      if self.lhs:
         result.append(self.lhs)
      if self.rhs:
         result.append(self.rhs)
      if self.modifications:
         result.append(self.modifications)
      result = [str(x) for x in result]
      if len(result) > 0:
         return 'Invocation(%s)' % ', '.join(result)
      else:
         return 'Invocation( )'

   ### FORMATTING ###

   @property
   def _opening(self):
      result = [ ]
      if self.lhs:
         cur = r'\new %s' % self.lhs
         if self.rhs:
            cur += ' = %s' % self.rhs
         if len(self.modifications) > 0:
            cur += r' \with {'
            result.append(cur)
            result.extend(['\t' + x for x in self.modifications])
            result.append('} %s' % self._client.brackets.open)
         else:
            cur += ' %s' % self._client.brackets.open
            result.append(cur)
      else:
         result.append(self._client.brackets.open)
      return result

   @property
   def _closing(self):
      result = [ ]
      result.append(self._client.brackets.close)
      return result
