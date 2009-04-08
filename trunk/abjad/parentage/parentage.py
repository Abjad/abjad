from abjad.core.interface import _Interface
from abjad.parentage.containment import _ContainmentSignature
from abjad.rational.rational import Rational
from abjad.receipt.parentage import _ParentageReceipt
import types


class _Parentage(_Interface):
   '''Serve literal score parentage information about component.
      Handle no LilyPond grob.'''

   def __init__(self, _client):
      '''Bind to client and set parent to None.'''
      _Interface.__init__(self, _client)
      self.__parent = None

   ## PRIVATE ATTRIBUTES ##
   
   @property
   def _governor(self):
      '''Return reference to first sequential container Q 
         in the parentage of client such that 
         the parent of Q is either a parallel container or None.
         In the case that no such sequential container exists
         in the parentage of client, return None.'''
      from abjad.container.container import Container
      for component in self.parentage:
         if isinstance(component, Container) and not component.parallel:
            parent = component.parentage.parent
            if parent is None:
               return component
            if isinstance(parent, Container) and parent.parallel:
               return component
            
   ## PRIVATE METHODS ##

   def _ignore(self):
      '''Client forgets parent (but parent remembers client).'''
      self.client._update._markForUpdateToRoot( )
      self.__parent = None

   ## TODO: Deprecate _Parentage._cut( ) receipt. Unnecessary. ##

   def _cut(self):
      '''Client and parent cut completely.'''
      client, parent = self.client, self.parent
      if parent is not None:
         index = parent.index(client)
         parent._music.remove(client)
      else:
         index = None
      self._ignore( )
      receipt = _ParentageReceipt(client, parent, index)
      return receipt

   def _first(self, klass):
      '''Return first instance of klass in score tree above client.'''
      for component in self.parentage[1:]:
         if isinstance(component, klass):
            return component

   ## TODO: Deprecate _Parentage._reattach( ) ##

   def _reattach(self, receipt):
      '''Reattach client to parent described in receipt.
         Empty receipt and return client.'''
      client = self._client
      assert client is receipt._component
      parent = receipt._parent
      index = receipt._index
      parent._music.insert(index, client)
      self.__parent = parent
      receipt._empty( )
      return client

   ## TODO: Rename _switchParentTo( ) to simply _Parentage._switch( ). ##

   def _switchParentTo(self, new_parent):
      '''Remove client from parent and give client to new_parent.'''
      self._cut( )
      self.__parent = new_parent
      self.client._update._markForUpdateToRoot( )

   ## PUBLIC ATTRIBUTES ##

   @property
   def depth(self):
      '''Absolute depth of component in Abjad expression.'''
      return len(self.parentage) - 1

   @property
   def layer(self):
      '''Layer of leaf in nested tuplet.'''
      from abjad.tuplet.tuplet import _Tuplet
      result = 0
      for parent in self.parentage[1:]:
         if isinstance(parent, _Tuplet):
            result += 1
      return result

   @property
   def orphan(self):
      '''True when component has no parent, otherwise False.'''
      return len(self.parentage) == 1

   @property
   def parent(self):
      '''Read-only reference to parent of client.'''
      return self.__parent
      
   @property
   def parentage(self):
      '''Return a list of all of elements in the
         parentage of client, including client.'''
      result = [ ]
      cur = self._client
      while cur is not None:
         result.append(cur)
         cur = cur.parentage.parent
      return result

   @property
   def root(self):
      '''Return reference to component at depth 0 of Abjad expression.'''
      return self.parentage[-1]

   @property
   def signature(self):
      '''Return _ContainmentSignature giving the root and
         first voice, staff and score in parentage of component.'''
      from abjad.score.score import Score
      from abjad.staffgroup.staffgroup import StaffGroup
      from abjad.staff.staff import Staff
      from abjad.voice.voice import Voice
      signature = _ContainmentSignature( )
      signature._self = self._client._ID
      for component in self._client.parentage.parentage:
         if isinstance(component, Voice) and not signature._voice:
            signature._voice = component._ID
         elif isinstance(component, Staff) and not signature._staff:
            signature._staff = component._ID
         elif isinstance(component, StaffGroup) and not signature._staffgroup:
            signature._staffgroup = component._ID
         elif isinstance(component, Score) and not signature._score:
            signature._score = component._ID
      else:
         '''Root components must be manifestly equal to compare True.'''
         signature._root = id(component)
         signature._root_str = component._ID
      return signature
