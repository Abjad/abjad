### TODO profile and figure out why Leaf.next and Leaf.prev
###      are taking so much time

### TODO decide if navigation should work only *within the voice*;
###      right now it's possible that Leaf.next will point
###      point to the next leaf in the following *staff*,
###      which is not what we want.

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
### where the note g, as the % goto @ comment suggests. would this 
### be overkill?

class Navigator(object):

   def __init__(self, client):
      self._client = client

   def _ascend(self):
      if hasattr(self._client, '_parent'):
         return self._client._parent
      else:
         return None

   def _rank(self):
      if hasattr(self._client, '_parent'):
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
            return self._client._ascend( )
      else:
         return self._client._ascend( )

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
