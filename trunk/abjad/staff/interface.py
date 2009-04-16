from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.formatcontributor import _FormatContributor
from abjad.core.observer import _Observer
from abjad.staff.staff import Staff
import types


class _StaffInterface(_Observer, _FormatContributor, _BacktrackingInterface):
   
   def __init__(self, _client, _updateInterface):
      _Observer.__init__(self, _client, _updateInterface)
      _FormatContributor.__init__(self)
      _BacktrackingInterface.__init__(self, 'staff')
      self._acceptableTypes = (Staff, types.NoneType)
      self._effective = None
      self._forced = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def before(self):
      '''Format contribution before leaf.'''
      result = [ ]
      if self.change or (not self.client.prev and self.forced):
         result.append(r'\change Staff = %s' % self.effective.name)
      return result

   @property
   def effective(self):
      effective = _BacktrackingInterface.effective.fget(self)
      if effective is None:
         from abjad.staff.staff import Staff
         for parent in self._client.parentage.parentage:
            if isinstance(parent, Staff):
               return parent
      return effective
