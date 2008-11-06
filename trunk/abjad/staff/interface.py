from abjad.core.interface import _Interface


class _StaffInterface(_Interface):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      self._forced = None

   @property
   def given(self):
      return self._client._parentage._first('Staff')

   @property
   def effective(self):
      return self._forced if self._forced else self.given
      
   @property
   def changed(self):
      return self._client.prev and \
         self._client.prev.staff != self._client.staff
      
   ### FORMATTING ###

   @property
   def _before(self):
      result = [ ]
      if self.changed or (not self._client.prev and self._forced):
         assert self.effective.invocation.name
         result.append(r'\change Staff = %s' % self.effective.invocation.name)
      return result

   @property
   def _after(self):
      '''Used only when very last note in staff is staff changed.'''
      result = [ ]
      if (self.changed or (not self._client.prev and self._forced)) and \
         not self._client.next:
         result.append(r'\change Staff = %s' % self.given.invocation.name)
      return result
