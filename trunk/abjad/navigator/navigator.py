from abjad.core.abjadcore import _Abjad
from collections import deque


### TODO profile and figure out why _Leaf.next and _Leaf.prev
###      are taking so much time

### TODO should we replace the old next with the new ._navigator._next?
###      add other next helpers such as nextLeaf?

class _Navigator(_Abjad):

   def __init__(self, client):
      self._client = client

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contemporaneousStartComponents(self):
      '''
      Return a list of all components in either the contents or
      parentage of client starting at the same moment as client,
      including client.
      '''
      result = [ ]
      result.extend(self._contemporaneousStartContents)
      result.extend(self._contemporaneousStartParentage)
      return list(set(result))
   
   @property
   def _contemporaneousStartContents(self):
      '''
      Return a list of all components in the contents of client
      starting at the same moment as client, including client.
      '''
      result = [ ]
      client = self._client
      result.append(client)
      if client.kind('Container'):
         if client.parallel:
            for x in client:
               result.extend(x._navigator._contemporaneousStartContents)
         elif len(client) > 0:
            result.extend(client[0]._navigator._contemporaneousStartContents)
      return result

   @property
   def _contemporaneousStartParentage(self):
      '''
      Return a list of all components in the parentage of client
      starting at the same moment as client, including client.
      '''
      client = self._client
      result = [client]
      prev = client
      for parent in client.parentage.parentage[1: ]:
         if parent.parallel:
            result.append(parent)
         elif parent.index(prev) == 0:
            result.append(parent)
         prev = parent
      return result

   @property
   def _contemporaneousStopComponents(self):
      '''
      Return a list of all components in either the contents or
      parentage of client stopping at the same moment as client,
      including client.
      '''
      result = [ ]
      result.extend(self._contemporaneousStopContents)
      result.extend(self._contemporaneousStopParentage)
      return list(set(result))
   
   @property
   def _contemporaneousStopContents(self):
      '''
      Return a list of all components in the contents of client
      stopping at the same moment as client, including client.
      '''
      result = [ ]
      client = self._client
      result.append(client)
      if client.kind('Container'):
         if client.parallel:
            client_duration = client.duration.preprolated
            for x in client:
               if x.duration.preprolated == client_duration:
                  result.extend(x._navigator._contemporaneousStopContents)
         elif len(client) > 0:
            result.extend(client[-1]._navigator._contemporaneousStopContents)
      return result

   @property
   def _contemporaneousStopParentage(self):
      '''
      Return a list of all components in the parentage of client
      stopping at the same moment as client, including client.
      '''
      client = self._client
      result = [client]
      prev = client
      for parent in client.parentage.parentage[1: ]:
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
   def _firstContainers(self):
      '''Returns the first (leftmost) container or containers 
         (in case there's a parallel structure) in the calling structure.'''
      if self._client.kind('Container'):
         containers = [ ]
         if self._client.parallel:
            for e in self._client:
               containers.extend(e._navigator._firstContainers)
         else:
            containers.append(self._client)
         return containers
      else:
         return [None]

   @property
   def _firstLeaves(self):
      '''
      Returns the first (leftmost) leaf or leaves 
      (in case there's a parallel structure) in a tree.
      '''
      if self._client.kind('_Leaf'):
         return [self._client]
      elif self._client.kind('Container'):
         leaves = [ ]
         if self._client.parallel:
            for e in self._client:
               leaves.extend(e._navigator._firstLeaves)
         elif len(self._client) > 0:
            leaves.extend(self._client[0]._navigator._firstLeaves)
         else:
            return [ ]
         return leaves
   
   @property
   def _lastLeaves(self):
      '''
      Returns the last (rightmost) leaf or leaves
      (in case there's a parallel structure) in a tree.
      '''
      if self._client.kind('_Leaf'):
         return [self._client]
      elif self._client.kind('Container'):
         leaves = [ ]
         if self._client.parallel:
            for e in self._client:
               leaves.extend(e._navigator._lastLeaves)
         elif len(self._client) > 0:
            leaves.extend(self._client[-1]._navigator._lastLeaves)
         else:
            return [ ]
         return leaves
      
   @property
   def _next(self):
      '''Returns next closest non-siamese Component.'''
      next = self._nextSibling
      if next:
         return next
      else:
         for p in self._client.parentage.parentage[1: ]:
            next = p._navigator._nextSibling
            if next:
               return next
      
   @property
   def _nextBead(self):
      '''Returns the next Bead (time threaded Leaf), if such exists. 
         This method will search the whole (parentage) structure moving forward.
         This will only return if called on a Leaf.'''
      if not self._client.kind('_Leaf'):
         return None
      next = self._next
      if next is None:
         return None
      candidates = next._navigator._firstLeaves
      return self._findFellowBead(candidates)

   @property
   def _nextLeaves(self):
      '''Returns list of next leaf/leaves regardless of "thread" or type 
         of caller. If next component is/contains a parallel, return list 
         of simultaneous leaves'''
      next = self._next
      if next:
         firstleaves = next._navigator._firstLeaves
         return firstleaves

   @property
   def _nextSibling(self):
      '''Returns the next *sequential* element in the caller's parent; 
         None otherwise'''
      rank = self._rank( )
      if (not rank is None) and (not self._client._parent.parallel): 
      # (parallels are siameses)
         if rank + 1 < len(self._client._parent._music):
            return self._client._parent._music[rank + 1]
      else:
         return None
         
   @property
   def _nextThread(self):
      '''Returns the next threadable Container.'''
      if not self._client.kind('Container'):
         return None
      next = self._next
      if next is None or next.kind('_Leaf'):
         return None
      containers = next._navigator._firstContainers
      for c in containers:
         if not c is None:
            if self._isThreadable(c):
               return c

   @property
   def _prev(self):
      '''Returns previous closest non-siamese Component.'''
      prev = self._prevSibling
      if prev:
         return prev
      else:
         for p in self._client.parentage.parentage[1: ]:
            prev = p._navigator._prevSibling
            if prev:
               return prev
      
   @property
   def _prevBead(self):
      '''Returns the previous Bead (time threaded Leaf), if such exists. 
         This method will search the whole (parentage) structure moving back.
         This will only return if called on a Leaf.'''
      if not self._client.kind('_Leaf'):
         return None
      prev = self._prev
      if prev is None:
         return None
      candidates = prev._navigator._lastLeaves
      return self._findFellowBead(candidates)

   @property
   def _prevLeaves(self):
      '''Returns list of previous leaf/leaves regardless of "thread" or type 
         of caller. If next component is/contains a parallel, return list 
         of simultaneous leaves'''
      prev = self._prev
      if prev:
         lastLeaves = prev._navigator._lastLeaves
         return lastLeaves

   @property
   def _prevSibling(self):
      '''Returns the previous *sequential* element in the caller's parent; 
         None otherwise'''
      rank = self._rank( )
      if (not rank is None) and (not self._client._parent.parallel): 
      # (parallels are siameses)
         if rank - 1 >= 0:
            return self._client._parent._music[rank - 1]
      else:
         return None

   ## PRIVATE METHODS ##

   # advance to self._client._music[rank], if possible;
   # otherwise ascend
   def _advance(self, rank):
      if hasattr(self._client, '_music'):
         if rank < len(self._client._music):
            return self._client._music[rank]
         else:
            return self._client._parent
      else:
         return self._client._parent

   def _findFellowBead(self, candidates):
      '''Helper method from prevBead and nextBead. 
      Given a list of bead candiates of self, find and return the first one
      that matches thread parentage. '''
      for candidate in candidates:
         if self._isThreadable(candidate):
            return candidate

   def _getImmediateTemporalSuccessors(self):
      cur = self._client
      while cur is not None:
         nextSibling = cur._navigator._nextSibling
         if nextSibling is None:
            cur = cur._parent
         else:
            return nextSibling._navigator._contemporaneousStartContents
      return [ ]

   def _hasGoodPath(self, arg):
      '''Returns True when all of the disjunct elements in the parentage
         of self._client and arg share the same context and when none
         of the disjunct elements in the parentage of self._client and arg
         are parallel containers.'''
      parentage = \
         self._client.parentage._disjunctInclusiveParentageBetween(arg)
      return not any([self._isInaccessibleToMe(p) for p in parentage])
      
   def _hasGoodSharedParent(self, arg):
      '''Returns True when self._client and arg have at least one
         element of shared parentage and the first element of shared
         parentage between self._client and arg is not parallel.'''
      first_shared = self._client.parentage._getFirstSharedParent(arg)
      return first_shared and not first_shared.parallel

   def _isImmediateTemporalSuccessorOf(self, expr):
      return expr in self._getImmediateTemporalSuccessors( )
         
   def _isInaccessibleToMe(self, arg):
      return getattr(arg, 'parallel', False) or \
         (hasattr(arg, 'invocation') and not self._shareContext(arg)) or \
         (hasattr(arg, 'invocation') and arg.invocation.name is None)

   def _isThreadable(self, expr):
      '''Check if expr is threadable with respect to self.'''
      c_thread_parentage = expr.parentage._threadParentage
      thread_parentage = self._client.parentage._threadParentage
      match_parent = True
      if len(c_thread_parentage) == len(thread_parentage):
         for c, p in zip(c_thread_parentage, thread_parentage):
            if type(c) == type(p):
               if c.kind('_Context') and p.kind('_Context'):
                  if c.invocation != p.invocation:
                     match_parent = False
      else:
         match_parent = False
      match_self = False
      if self._client.kind('_Leaf') and expr.kind('_Leaf'):
         match_self = True
      elif self._client.kind('Container') and expr.kind('Container'):
         if not self._client.parallel and not expr.parallel:
            if self._client.kind('_Context') and expr.kind('_Context'):
               if self._client.invocation == expr.invocation:
                  match_self =  True
            elif type(self._client) == type(expr):
               match_self =  True
      return match_self and match_parent

   # rightwards depth-first traversal:
   # advance rightwards; otherwise ascend; otherwise None.
   # return next node yet-to-be visited, last rank already visited
   def _nextNodeHelper(self, lastVisitedRank = None):
      if hasattr(self._client, '_music'):
         if lastVisitedRank is None:
            if len(self._client._music) > 0:
               return self._client._music[0], None
            else:
               return None, None
         else:
            if lastVisitedRank + 1 < len(self._client._music):
               return self._client._music[lastVisitedRank + 1], None
            elif self._client._parent:
               return self._client._parent, self._rank( )
            else:
               return None, None
      elif self._client._parent:
         return self._client._parent, self._rank( )
      else:
         return None, None

   def _pathExistsBetween(self, arg):
      '''Returns True when self._client and arg are ultimately contained
         in the same expression, when a reference pathway exists between
         self._client and arg that passes over no \new or \context
         boundaries, and when a reference path exists between self._client
         and arg that crosses over no parallel containers.
         
         I propose replacing _isThreadable with this method.'''
      return self._hasGoodSharedParent(arg) and self._hasGoodPath(arg)

   # leftwards depth-first traversal;
   # return next node yet-to-be visited, last rank already visited
   def _prevNodeHelper(self, lastVisitedRank = None):
      if hasattr(self._client, '_music'):
         if lastVisitedRank == None:
            if len(self._client._music) > 0:
               return self._client._music[-1], None
            else:
               return None, None
         else:
            if lastVisitedRank > 0:
               return self._client._music[lastVisitedRank - 1], None
            elif self._client._parent:
               return  self._client._parent, self._rank( )
            else:
               return None, None
      elif not hasattr(self._client, '_parent'):
         print 'WARNING: node without parent!'
         print self._client.lily
         print ''
         raise Exception
      elif self._client._parent:
         return self._client._parent, self._rank( )
      else:
         return None, None

   def _rank(self):
      '''Returns the index of the caller (its position) in 
         the parent container. If caller has no parent, 
         returns None.'''
      if not self._client._parent is None:
         return self._client._parent._music.index(self._client)
      else:
         return None

   def _shareContext(self, arg):
      '''Return True when self._client and arg share the same
         enclosing context name, otherwise False.'''
      return self._client.parentage._enclosingContextName == \
         arg.parentage._enclosingContextName

   def _traverse(self, v, depthFirst=True, leftRight=True):
      if depthFirst:
         self._traverseDepthFirst(v)
      else:
         self._traverseBreadthFirst(v, leftRight)

   def _traverseBreadthFirst(self, v, leftRight = True):
      queue = deque([self._client])
      while queue:
         node = queue.popleft( )
         v.visit(node)
         if hasattr(node, '_music'):
            if leftRight:
               queue.extend(node._music)
            else:
               queue.extend(reversed(node._music))

   def _traverseDepthFirst(self, v):
      v.visit(self._client)
      if hasattr(self._client, '_music'):
         for m in self._client._music:
            m._navigator._traverse(v)
      if hasattr(v, 'unvisit'):
         v.unvisit(self._client)

   ## DEPTH-FIRST SEARCH STUFF BELOW #####
   ## TODO - ISOLATE IN SEPARATE MODULE ##

   def _nextNodeDF(self, total):
      '''
      If client has unvisited music, 
      return next unvisited node in client's music.

      If client has no univisited music and has a parent,
      return client's parent.

      If client has no univisited music and no parent,
      return None.
      '''

      client = self._client
      if hasattr(client, '_music') and len(client) > 0 and \
         total < len(client):
         return client[total], 0 
      else:
         parent = client._parent
         if parent is not None:
            return parent, parent.index(client) + 1
         else:
            return None, None

   def _prevNodeDF(self, total = 0):
      '''
      If client has unvisited music, 
      return prev unvisited node in client's music.

      If client has no univisited music and has a parent,
      return client's parent.

      If client has no univisited music and no parent,
      return None.
      '''

      client = self._client
      if hasattr(client, '_music') and len(client) > 0 and \
         total < len(client):
         return client[len(client) - 1 - total], 0
      else:
         parent = client._parent
         if parent is not None:
            return parent, len(parent) - parent.index(client)
         else:
            return None, None

   def _DFS(self, capped = True, unique = True, 
      forbid = None, direction = 'left'):
      client_parent, node, rank = self._client._parent, self._client, 0 
      queue = deque([ ])
      while node is not None and not (capped and node is client_parent):
         result = self._findYield(node, rank, queue, unique)
         if result is not None:
            yield result
         if self._isNodeForbidden(node, forbid):
            node, rank = self._handleForbiddenNode(node, queue)
         else:
            node, rank = self._advanceNodeDF(node, rank, direction)
      queue.clear( )

   def _handleForbiddenNode(self, node, queue):
      node_parent = node._parent
      if node_parent is not None:
         rank = node_parent.index(node) + 1
         node = node_parent
      else:
         node, rank = None, None
      queue.pop( )
      return node, rank

   def _advanceNodeDF(self, node, rank, direction):
      if direction == 'left':
         node, rank = node._navigator._nextNodeDF(rank)
      else:
         node, rank = node._navigator._prevNodeDF(rank)
      return node, rank

   def _isNodeForbidden(self, node, forbid):
      if forbid is None:
         return False
      elif isinstance(forbid, str):
         return node.kind(forbid)
      else:
         return any([node.kind(x) for x in forbid])

   def _findYield(self, node, rank, queue, unique):
      if hasattr(node, '_music'):
         try:
            visited = node is queue[-1]
         except IndexError:
            visited = False
         if not visited or unique is not True:
            queue.append(node)
            return node
         elif rank == len(node):
            queue.pop( )
            return None
      else:
         return node
