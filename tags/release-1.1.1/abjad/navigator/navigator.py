from abjad.core.abjadcore import _Abjad
#from abjad.navigator.dfs import depth_first_search
import collections


class _Navigator(_Abjad):

   def __init__(self, client):
      self._client = client

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contemporaneousStartComponents(self):
      '''Return a list of all components in either the contents or
         parentage of client starting at the same moment as client,
         including client.'''
      result = [ ]
      result.extend(self._contemporaneousStartContents)
      result.extend(self._contemporaneousStartParentage)
      return list(set(result))
   
   @property
   def _contemporaneousStartContents(self):
      '''Return a list of all components in the contents of client
         starting at the same moment as client, including client.'''
      from abjad.container import Container
      result = [ ]
      client = self._client
      result.append(client)
      if isinstance(client, Container):
         if client.parallel:
            for x in client:
               result.extend(x._navigator._contemporaneousStartContents)
         #elif len(client) > 0:
         elif len(client):
            result.extend(client[0]._navigator._contemporaneousStartContents)
      return result

   @property
   def _contemporaneousStartParentage(self):
      '''Return a list of all components in the parentage of client
         starting at the same moment as client, including client.'''
      client = self._client
      result = [client]
      prev = client
      for parent in client.parentage.parentage[1:]:
         if parent.parallel:
            result.append(parent)
         elif parent.index(prev) == 0:
            result.append(parent)
         prev = parent
      return result

   @property
   def _contemporaneousStopComponents(self):
      '''Return a list of all components in either the contents or
         parentage of client stopping at the same moment as client,
         including client.'''
      result = [ ]
      result.extend(self._contemporaneousStopContents)
      result.extend(self._contemporaneousStopParentage)
      return list(set(result))
   
   @property
   def _contemporaneousStopContents(self):
      '''Return a list of all components in the contents of client
         stopping at the same moment as client, including client.'''
      from abjad.container import Container
      result = [ ]
      client = self._client
      result.append(client)
      if isinstance(client, Container):
         if client.parallel:
            client_duration = client.duration.preprolated
            for x in client:
               if x.duration.preprolated == client_duration:
                  result.extend(x._navigator._contemporaneousStopContents)
         #elif len(client) > 0:
         elif len(client):
            result.extend(client[-1]._navigator._contemporaneousStopContents)
      return result

   @property
   def _contemporaneousStopParentage(self):
      '''Return a list of all components in the parentage of client
         stopping at the same moment as client, including client.'''
      client = self._client
      result = [client]
      prev = client
      for parent in client.parentage.parentage[1:]:
         if parent.parallel:
            if prev.duration.prolated == parent.duration.prolated:
               result.append(parent)
            else:
               break
         elif parent.index(prev) == len(parent) - 1:
            result.append(parent)
         prev = parent
      return result


   @property
   def _firstLeaves(self):
      '''Returns the first (leftmost) leaf or leaves 
         (in case there's a parallel structure) in a tree.'''
      from abjad.container import Container
      from abjad.leaf.leaf import _Leaf
      client = self._client
      if isinstance(client, _Leaf):
         return [client]
      elif isinstance(client, Container):
         leaves = [ ]
         if self._client.parallel:
            for e in self._client:
               leaves.extend(e._navigator._firstLeaves)
         #elif len(self._client) > 0:
         elif len(self._client):
            leaves.extend(self._client[0]._navigator._firstLeaves)
         else:
            return [ ]
         return leaves
   
   @property
   def _lastLeaves(self):
      '''Returns the last (rightmost) leaf or leaves
         (in case there's a parallel structure) in a tree.'''
      from abjad.container import Container
      from abjad.leaf.leaf import _Leaf
      client = self._client
      if isinstance(client, _Leaf):
         return [client]
      elif isinstance(client, Container):
         leaves = [ ]
         if self._client.parallel:
            for e in self._client:
               leaves.extend(e._navigator._lastLeaves)
         #elif len(self._client) > 0:
         elif len(self._client):
            leaves.extend(self._client[-1]._navigator._lastLeaves)
         else:
            return [ ]
         return leaves
      
   @property
   def _next(self):
      '''Returns next Component in temporal order.'''
      next = self._nextSibling
      if next:
         return next
      else:
         for p in self._client.parentage.parentage[1:]:
            next = p._navigator._nextSibling
            if next:
               return next
      
   @property
   def _nextBead(self):
      '''Returns the next Bead (time threaded Leaf), if such exists. 
         This method will search the whole (parentage) structure 
         moving forward.
         This will only return if called on a Leaf.'''
      from abjad.leaf.leaf import _Leaf
      if not isinstance(self._client, _Leaf):
         return None
      next = self._next
      if next is None:
         return None
      candidates = next._navigator._firstLeaves
      return self._findFellowBead(candidates)

   @property
   def _nextNamesake(self):
      '''Find the next Component of the same type and with the same 
      parentage signature.'''
      next = self._next
      if next is None:
         return None
      for node in next._navigator._DFS(capped = False):
         if type(node) == type(self._client) and \
            node.parentage.signature == self._client.parentage.signature:
            return node

   ## TODO: Write tests for _Navigator._prevNamesake.               ##
   ##       Backwards DFS has always had a bug that needs fixing. ##

   @property
   def _prevNamesake(self):
      '''Find the prev component of same type and parentage signature.'''
      prev = self._prev
      if prev is None:
         return None
      for node in prev._navigator._DFS(capped = False, direction = 'right'):
         if type(node) == type(self._client) and \
            node.parentage.signature == self._client.parentage.signature:
            return node

   @property
   def _nextSibling(self):
      '''Returns the next *sequential* element in the caller's parent; 
      None otherwise'''
      rank = self._rank( )
      if (not rank is None) and (not self._client.parentage.parent.parallel): 
         if rank + 1 < len(self._client.parentage.parent._music):
            return self._client.parentage.parent._music[rank + 1]
      else:
         return None
         
   @property
   def _nextThread(self):
      '''Returns the next threadable Container.'''
      from abjad.container import Container
      from abjad.leaf.leaf import _Leaf
      if not isinstance(self._client, Container):
         return None
      next = self._next
      if next is None or isinstance(next, _Leaf):
         return None
      containers = next._navigator._contemporaneousStartComponents
      for c in containers:
         if self._isThreadable(c):
            return c

   @property
   def _prev(self):
      '''Returns previous Component in temporal order.'''
      prev = self._prevSibling
      if prev:
         return prev
      else:
         for p in self._client.parentage.parentage[1:]:
            prev = p._navigator._prevSibling
            if prev:
               return prev
      
   @property
   def _prevBead(self):
      '''Returns the previous Bead (time threaded Leaf), if such exists. 
         This method will search the whole (parentage) structure moving back.
         This will only return if called on a Leaf.'''
      from abjad.leaf.leaf import _Leaf
      if not isinstance(self._client, _Leaf):
         return None
      prev = self._prev
      if prev is None:
         return None
      candidates = prev._navigator._lastLeaves
      return self._findFellowBead(candidates)

   @property
   def _prevSibling(self):
      '''Returns the previous *sequential* element in the caller's parent; 
         None otherwise'''
      rank = self._rank( )
      if (not rank is None) and (not self._client.parentage.parent.parallel): 
         if rank - 1 >= 0:
            return self._client.parentage.parent._music[rank - 1]
      else:
         return None

   ## PRIVATE METHODS ##

   def _advance(self, rank):
      '''Advance to self._client._music[rank], if possible,
         otherwise ascend.'''
      if hasattr(self._client, '_music'):
         if rank < len(self._client._music):
            return self._client._music[rank]
         else:
            return self._client.parentge.parent
      else:
         return self._client.parentage.parent

   def _DFS(self, capped = True, unique = True, 
      forbid = None, direction = 'left'):
      from abjad.tools import iterate
      #return depth_first_search(
      #   self._client, capped, unique, forbid, direction)
      return iterate.depth_first(
         self._client, capped, unique, forbid, direction)

   def _findFellowBead(self, candidates):
      '''Helper method from prevBead and nextBead. 
         Given a list of bead candiates of self, find and return the first one
         that matches thread parentage. '''
      for candidate in candidates:
         if self._isThreadable(candidate):
            return candidate

   def _getImmediateTemporalSuccessors(self):
      '''Return Python list of components immediately after self._client.'''
      cur = self._client
      while cur is not None:
         nextSibling = cur._navigator._nextSibling
         if nextSibling is None:
            cur = cur.parentage.parent
         else:
            return nextSibling._navigator._contemporaneousStartContents
      return [ ]

   def _isImmediateTemporalSuccessorOf(self, expr):
      '''True when client follows immediately after expr,
         otherwise False.'''
      return expr in self._getImmediateTemporalSuccessors( )
         
   def _isThreadable(self, expr):
      '''Check if expr is threadable with respect to self.'''
      from abjad.tools import check
      return check.assess_components([self._client, expr], share = 'thread')

   ## TODO: Move _Navigator._rank to Parentage._rank ##

   def _rank(self):
      '''Returns the index of the caller (its position) in 
         the parent container. If caller has no parent, 
         returns None.'''
      parent = self._client.parentage.parent
      if parent is not None:
         return parent._music.index(self._client)
      else:
         return None

   def _traverse(self, v, depthFirst=True, leftRight=True):
      '''Traverse with visitor visiting each node in turn.'''
      if depthFirst:
         self._traverseDepthFirst(v)
      else:
         self._traverseBreadthFirst(v, leftRight)

   def _traverseBreadthFirst(self, v, leftRight = True):
      '''Traverse breadth-first with visitor visiting each node.'''
      queue = collections.deque([self._client])
      while queue:
         node = queue.popleft( )
         v.visit(node)
         if hasattr(node, '_music'):
            if leftRight:
               queue.extend(node._music)
            else:
               queue.extend(reversed(node._music))

   def _traverseDepthFirst(self, v):
      '''Traverse depth-frist with visitor visiting each node.'''
      v.visit(self._client)
      if hasattr(self._client, '_music'):
         for m in self._client._music:
            m._navigator._traverse(v)
      if hasattr(v, 'unvisit'):
         v.unvisit(self._client)
