from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.formatcontributor import _FormatContributor
from abjad.core.interface import _Interface
import types


class _StaffInterface(_Interface, _FormatContributor, _BacktrackingInterface):
   
   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
      _BacktrackingInterface.__init__(self, 'staff.effective')
      self._forced = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      '''Format contribution after leaf.
         Used only when very last note in staff is staff changed.'''
      result = [ ]
      if (self.change or (not self.client.prev and self.forced)) and \
         not self.client.next:
         result.append(r'\change Staff = %s' % self.given.name)
      return result

   @property
   def before(self):
      '''Format contribution before leaf.'''
      result = [ ]
      if self.change or (not self.client.prev and self.forced):
         result.append(r'\change Staff = %s' % self.effective.name)
      return result

   @property
   def effective(self):
      '''Effective staff of client.'''
      return self.forced if self.forced else self.given

   @apply
   def forced( ):
      '''Read / write value to force staff change here.'''
      from abjad.staff.staff import Staff
      def fget(self):
         return self._forced
      def fset(self, arg):
         assert isinstance(arg, (Staff, types.NoneType))
         self._forced = arg

   @property
   def given(self):
      '''First staff in score parentage of client.'''
      from abjad.staff.staff import Staff
      return self.client.parentage.first(Staff)
