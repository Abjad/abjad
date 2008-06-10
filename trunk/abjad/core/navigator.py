### TODO profile and figure out why _Leaf.next and _Leaf.prev
###      are taking so much time

### TODO decide if navigation should work only *within the voice*;
###      right now it's possible that _Leaf.next will point
###      point to the next leaf in the following *staff*,
###      which is not what we want.
### TODO should we replace the old next with the new ._navigator._next?
###      add other next helpers such as nextLeaf?

### Hmm, this is an interesting one because, considering the use of 
### \context instead of \new as we've mentioned before, you may have 
### a sequence of two staffs with the same name (i.e. referencing the 
### same lily object) with their own voices, which may in turn also 
### reference the same objects. e.g.
### {
###    \context Staff='mystaff' {
###       <<
###          \context Voice='v_low' {
###             c8 d e f % goto @
###             }
###          \context Voice='v_high' {
###             c'8 d' e' f'
###             }
###       >>
###    }
###    \context Staff='mystaff' {
###       \context Voice='v_low' {
###          % @
###          g a b c'
###          }
###    }
### 
### }
###
### it'd be nice if the next note of the note f in voice 'v_low' 
### where the note g, as the % goto @ comment suggests. 
### This is now implemented!!! works great! 
### Not public yet thought. To navigate, use: Leaf._navigator._nextBead. 


class _Navigator(object):

   def __init__(self, client):
      self._client = client

   def _rank(self):
      '''Returns the index of the caller (its position) in the parent container.
         If caller has no parent, returns None.'''
      #if hasattr(self._client, '_parent'):
      if not self._client._parent is None:
         return self._client._parent._music.index(self._client)
      else:
         return None

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

   @property
   def _firstLeaves(self):
      '''Returns the first (leftmost) leaf or leaves 
         (in case there's a parallel structure) in a tree.'''
      if self._client.kind('_Leaf'):
         return [self._client]
      elif self._client.kind('Container'):
         leaves = [ ]
         if self._client.parallel:
            for e in self._client:
               leaves.extend(e._navigator._firstLeaves)
         else:
            #print self._client
            leaves.extend(self._client[0]._navigator._firstLeaves)
         return leaves
   
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

   @property
   def _next(self):
      '''Returns next closest non-siamese Component.'''
      next = self._nextSibling
      if next:
         return next
      else:
         for p in self._client._parentage._parentage:
            next = p._navigator._nextSibling
            if next:
               return next
      
   @property
   def _prev(self):
      '''Returns previous closest non-siamese Component.'''
      prev = self._prevSibling
      if prev:
         return prev
      else:
         for p in self._client._parentage._parentage:
            prev = p._navigator._prevSibling
            if prev:
               return prev
      
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
      for candidate in candidates:
         c_thread_parentage = candidate._parentage._threadParentage
         thread_parentage = self._client._parentage._threadParentage
         #print thread_parentage
         #print c_thread_parentage
         ### check that parentages match.
         match = True
         if len(c_thread_parentage) == len(thread_parentage):
            for c, p in zip(c_thread_parentage, thread_parentage):
               if type(c) == type(p):
                  if c.kind('Context') and p.kind('Context'):
                     if c.invocation != p.invocation:
                        match = False
         else:
            match = False

         if match:
            return candidate


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

   def _traverse(self, v):
      v.visit(self._client)
      if hasattr(self._client, '_music'):
         for m in self._client._music:
            m._navigator._traverse(v)
      if hasattr(v, 'unvisit'):
         v.unvisit(self._client)
