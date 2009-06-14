from abjad.core.backtracking import _BacktrackingInterface
from abjad.core.formatcontributor import _FormatContributor
from abjad.core.observer import _Observer
import types


## TODO: Make _StaffInterface handle LilyPond StaffSymbol grob? ##

class _StaffInterface(_Observer, _FormatContributor, _BacktrackingInterface):
   r'''Report on Abjad staff in parentage of client.
      Interface to LilyPond \stopStaff, \startStaff hiding commands.
      Handle no LilyPond grob.'''
   
   def __init__(self, _client, _updateInterface):
      '''Register as observer, format contributor and backtracker.
         Init effective and force staff to None.
         Init hide to False.'''
      from abjad.staff import Staff
      _Observer.__init__(self, _client, _updateInterface)
      _FormatContributor.__init__(self)
      _BacktrackingInterface.__init__(self, 'staff')
      self._acceptableTypes = (Staff, types.NoneType)
      self._effective = None
      self._forced = None
      self._hide = False

   ## PUBLIC ATTRIBUTES ##

   @property
   def closing(self):
      '''Format contribution at container closing or after leaf.'''
      result = [ ]
      if self.hide:
         result.append(r'\startStaff')
      return result

   @property
   def effective(self):
      '''Effective staff of client.
         If staff is forced on client, return forced staff.
         Otherwise, return explicit staff of client.'''
      effective = _BacktrackingInterface.effective.fget(self)
      if effective is None:
         return self.explicit
      return effective

   @property
   def explicit(self):
      '''First explicit *Abjad* ``Staff`` in parentage of client.
         Otherwise ``None``.'''
      from abjad.staff import Staff
      for parent in self._client.parentage.parentage:
         if isinstance(parent, Staff):
            return parent

   @apply
   def hide( ):
      r'''Interface to LilyPond \stopStaff, \startStaff commands.'''
      def fget(self):
         return self._hide
      def fset(self, arg):
         assert isinstance(arg, (types.BooleanType, types.NoneType))
         self._hide = arg
      return property(**locals( ))

   ## TODO: Client type-testing in _StaffInterface is a hack. ##
   ##       Replace eventually with something structural.     ##

   @property
   def opening(self):
      '''Format contribution at container opening or before leaf.'''
      from abjad.leaf.leaf import _Leaf
      from abjad.tools import iterate
      result = [ ]
      ## if client is a leaf
      if isinstance(self._client, _Leaf):
         if self.change or (not self.client.prev and self.forced):
            result.append(r'\change Staff = %s' % self.effective.name)
      ## if client is a measure
      else:
         try:
            prev = iterate.measure_prev(self.client)
         except:
            prev = None
         if self.change or (prev is None and self.forced):
            result.append(r'\change Staff = %s' % self.effective.name)
      if self.hide:
         result.append(r'\stopStaff')
      return result
