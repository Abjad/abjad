from .. core.interface import _Interface

class StaffInterface(_Interface):
   
   def __init__(self, client):
      _Interface.__init__(self, client, 'Staff', ['Staff'])
      self.forced = None

   @property
   def given(self):
      return self._client._parentage._first('Staff')

   @property
   def effective(self):
      return self.forced if self.forced else self.given
      
   @property
   def changed(self):
      return self._client.prev and \
         self._client.prev.staff != self._client.staff
      
   ### FORMATTING ###

   @property
   def _before(self):
      result = [ ]
      if self.changed or (not self._client.prev and self.forced):
         assert self.effective.invocation.rhs
         result.append(r'\change Staff = %s' % self.effective.invocation.rhs)
      return result

   @property
   def _after(self):
      '''Used only when very last note in staff is staff changed.'''
      result = [ ]
      if (self.changed or (not self._client.prev and self.forced)) and \
         not self._client.next:
         result.append(r'\change Staff = %s' % self.given.invocation.rhs)
      return result
