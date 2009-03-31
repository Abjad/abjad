from abjad.core.formatcarrier import _FormatCarrier
from abjad.core.interface import _Interface


class _StaffInterface(_Interface, _FormatCarrier):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatCarrier.__init__(self)
      self._forced = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _before(self):
      result = [ ]
      if self.changed or (not self._client.prev and self._forced):
         result.append(r'\change Staff = %s' % self.effective.name)
      return result

   @property
   def _after(self):
      '''Used only when very last note in staff is staff changed.'''
      result = [ ]
      if (self.changed or (not self._client.prev and self._forced)) and \
         not self._client.next:
         result.append(r'\change Staff = %s' % self.given.name)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def changed(self):
      return self._client.prev and \
         self._client.prev.staff != self._client.staff

   @property
   def effective(self):
      return self._forced if self._forced else self.given

   @property
   def given(self):
      from abjad.staff.staff import Staff
      return self._client.parentage._first(Staff)
