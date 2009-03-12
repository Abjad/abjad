from abjad.core.abjadcore import _Abjad
from abjad.rational.rational import Rational
from abjad.receipt.parentage import _ParentageReceipt


class _Parentage(_Abjad):

   def __init__(self, client):
      self._client = client

   ## PRIVATE ATTRIBUTES ##
   
   @property
   def _enclosingContextName(self):
      '''Return invocation name of context 
         closest to client in score tree.'''
      for p in self.parentage:
         invocation = getattr(p, 'invocation', None)
         if invocation:
            return invocation.name
      else:
         return None

   @property
   def _governor(self):
      '''Return a reference to the first 
         sequential container enclosing client.'''
      p = self._client._parent
      if p is None or p.parallel:
         return None
      while p._parent is not None and not p._parent.parallel:
         p = p._parent
      return p

   @property
   def _threadParentage(self):
      '''Return thread-pertinent parentage structure.
         Same as _parentage but with _Tuplets, redundant Sequentials, 
         Parallels and tautologies (unlikely) removed.'''
      from abjad.container.parallel import Parallel
      from abjad.container.sequential import Sequential
      from abjad.context.context import _Context
      from abjad.tuplet.tuplet import _Tuplet
      parentage = self.parentage[1:]
      if len(parentage) > 0:
      ## remove sequentials
         for p in parentage[:]:
            if isinstance(p, (Sequential, _Tuplet)):
               parentage.remove(p)
            else:
               break
      # remove tautological nesting
         for i, p in enumerate(parentage[:-1]):
            if type(p) == type(parentage[i+1]):
               if isinstance(p, Parallel):
                  parentage.remove(p)
               elif isinstance(p, _Context):
                  if p.invocation == parentage[i+1].invocation:
                     parentage.remove(p)
      return parentage

   ## PRIVATE METHODS ##

   def _cutOutgoingReferenceToParent(self):
      '''Keep incoming reference from parent to client in tact.
         Sever ougoing reference from parent to client.
         Parent will continue to reference client.
         Client will no longer reference parent.
         Return parent.'''
      if hasattr(self._client, '_parent'):
         parent = self._client._parent
         self._client._parent = None
         return parent

   def _detach(self):
      '''Sever incoming reference from parent to client.
         Sever outgoing reference from client to parent.'''
      client = self._client
      client._update._markForUpdateToRoot( )
      parent, index = self._removeFromParent( )
      self._cutOutgoingReferenceToParent( )
      receipt = _ParentageReceipt(client, parent, index)
      return receipt


   def _disjunctInclusiveParentageBetween(self, arg):
      '''Same as _disjunctParentageBetween( ) but including
         references to self._client and arg.'''
      return set(self.parentage) ^ set (arg.parentage.parentage)

   def _first(self, classname):
      '''Return first instance of classname 
         in score tree above client.'''
      p = self._client._parent
      while p is not None:
         if p.kind(classname):
            return p
         else:
            p = p._parent
      return None

   def _getFirstSharedParent(self, arg):
      '''Returns first shared parent between self._client and arg,
         otherwise None.'''
      shared = set(self.parentage) & set(arg.parentage.parentage)
      if shared:
         for parent in self.parentage:
            if parent in shared:
               return parent
      return None

   def _reattach(self, receipt):
      '''Reattach client to parent described in receipt.
         Empty receipt and return client.'''
      client = self._client
      assert client is receipt._component
      parent = receipt._parent
      index = receipt._index
      parent._music.insert(index, client)
      client._parent = parent
      receipt._empty( )
      return client

   def _removeFromParent(self):
      '''Sever incoming reference from parent to client.
         Leave outgoing reference from client to parent in tact.
         Parent will no longer reference client.
         Client will continue to reference parent.'''
      client = self._client
      if hasattr(client, '_parent'):
         try:
            parent = self.parent
            index = parent.index(client)
            parent._music.remove(client)
            return parent, index
         ## TODO: Filter this except
         except:
            pass
      return None, None

   def _splice(self, components):
      '''Insert components immediately after self in parent.
         Do not handle spanners.'''
      if self.parent is not None:
         client = self._client
         index = self.parent.index(client) + 1
         self.parent[index:index] = components
         return [client] + components

   def _switchParentTo(self, new_parent):
      '''Remove client from parent and give client to new_parent.'''
      client = self._client
      old_parent = client._parent
      if old_parent is not None:
         old_parent._music.remove(client)
      client._parent = new_parent

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

   ## TODO: Reimplement self._client._parent as self._parent

   @property
   def parent(self):
      '''Return reference to parent of client, else None.'''
      return self._client._parent
      
   @property
   def parentage(self):
      '''Return a list of all of elements in the
      parentage of client, including client.'''
      result = [ ]
      cur = self._client
      while cur is not None:
         result.append(cur)
         cur = cur._parent
      return result

   @property
   def root(self):
      '''Return reference to component at depth 0 of Abjad expression.'''
      return self.parentage[-1]
