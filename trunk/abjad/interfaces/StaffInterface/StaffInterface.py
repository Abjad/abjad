from abjad.core import _BacktrackingInterface
from abjad.interfaces._Observer import _Observer
import types


class StaffInterface(_Observer, _BacktrackingInterface):
   r'''Report on Abjad staff in parentage of client.
   Interface to LilyPond \stopStaff, \startStaff hiding commands.
   Interface to LilyPond fontSize context setting.
   Handle no LilyPond StaffSymbol grob.
   '''
   
   def __init__(self, _client, _updateInterface):
      '''Register as observer, format contributor and backtracker.
      Init effective and force staff to None.
      Init hide to False.'''
      from abjad.components.Staff import Staff
      _Observer.__init__(self, _client, _updateInterface)
      _BacktrackingInterface.__init__(self, 'staff')
      self._acceptableTypes = (Staff, )
      self._effective = None
      self._font_size = None
      self._forced = None
      self._hide = None
      self._show = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _closing(self):
      '''Format contribution at container closing or after leaf.'''
      result = [ ]
      if self.hide:
         result.append(r'\startStaff')
      elif self.show:
         result.append(r'\stopStaff')
      return result

   ## TODO: Client type-testing in StaffInterface is a hack. ##
   ##       Replace eventually with something structural.     ##

   @property
   def _opening(self):
      '''Format contribution at container opening or before leaf.'''
      from abjad.components._Leaf import _Leaf
      from abjad.tools import measuretools
      result = [ ]
      ## if client is a leaf
      if isinstance(self._client, _Leaf):
         if self.change or (not self._client.prev and self.forced):
            result.append(r'\change Staff = %s' % self.effective.name)
      ## if client is a measure
      else:
         try:
            prev = measuretools.get_prev_measure_from_component(self._client)
         except:
            prev = None
         if self.change or (prev is None and self.forced):
            result.append(r'\change Staff = %s' % self.effective.name)
      if self.hide:
         result.append(r'\stopStaff')
      elif self.show:
         result.append(r'\startStaff')
      return result

   ## PUBLIC ATTRIBUTES ##

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
      '''First explicit Abjad staff in parentage of client.
      Otherwise none.'''
      from abjad.components.Staff import Staff
      for parent in self._client.parentage.parentage:
         if isinstance(parent, Staff):
            return parent

   @apply
   def hide( ):
      r'''Interface to LilyPond \stopStaff, \startStaff commands,
      in that order.'''
      def fget(self):
         return self._hide
      def fset(self, arg):
         assert isinstance(arg, (types.BooleanType, type(None)))
         if self.show is not None:
            raise ValueError('can not set hide and show at same time.')
         self._hide = arg
      return property(**locals( ))
   
   @apply
   def show( ):
      r'''Interface to LilyPond \startStaff and \stopStaff commands,
      in that order.'''
      def fget(self):
         return self._show
      def fset(self, arg):
         assert isinstance(arg, (types.BooleanType, type(None)))
         if self.hide is not None:
            raise ValueError('can not set show and hide at same time.')
         self._show = arg
      return property(**locals( ))
