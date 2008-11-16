# Class: Spanner( )

# Spanners model one of three things:
# 1. (grob) overrides such as (Stem, direction, down);
# 2. (context) settings, such as (Score, currentBarNumber, 32);
# 3. (start / stop) indicators such as beam [ start and ] stop;
# LilyPond refers to (grob) overrides and (context) settings;
# the term 'indicator' to refer to [ ] and ( ) and so on is new here;
# we call overrides, settings and indicators collectively 'directives'.

# This abstract spanner baseclass implements a 'receptors' list;
# spanner subclasses include Override, _Setting, BeamSpanner, etc.

# _Leaf components include Duration, Beam, Stem, etc.;
# spanner receptors are a special type of leaf component;
# spanner receptors include Beam, Stem, etc. but not Duration;
# receptors reference spanners; other leaf components don't.

# A single receptor may participate in many receptors;
# l.stem.spanners, for example, may reference two overrides and a setting.

# Arity relationships:
#     spanners carry exactly one directive
#     spanners 'have' zero to many (leaf component) receptors
#     some leaf components 'reference' no spanners
#     other leaf components 'reference' one or more spanners
#     (leaf) components 'have' exactly one (leaf) target
#     leaves 'have' many predefined (leaf) components

# Spanners reference only contiguous receptors;
# this criterion engenders a spanner well-formedness test.

# Spanners 'block' incoming references and 'remove' outgoing references;
# spanners first block and then remove to 'sever' a receptor.

# The abstract spanner baseclass produces no LilyPond input;
# overrides, settings and indicators know how to format themselves;
# concrete directives inspect their receptors at format-time;
# concrete directives build before, after, left, right at format-time;
# receptors collate directive formatting at format-time;
# receptors sometimes add additional formatting at format-time;
# receptors hand over complete formatting to leaf at format-time.

# Two spanner 'match' when grobs, attributes and values correspond.

# A single spanner may 'fracture' into two new spanners;
# spanner fracturation generates a 'receipt' triple;
# fracturation receipts comprise ((blocking) source, left, right);
# hold on to the receipt to undo.

# Two spanners may 'fuse' to produce a new spanner;
# only matching spanners which follow one another may fuse;
# spanner fusion generates a 'receipt' triple;
# fusion receipts comprise ((blocking) left, (blocking) right, target);
# hold on to the receipt to undo.

### PUBLIC INTERFACE
###
###        capture( )
###        copy( )
###        die( )
###        duration( )
###        fracture( )
###        fuse( )
###        move( )
###        surrender( )

###  TODO  make index( ) private.
###        reimplement capture / surrender to left / right.

from abjad.rational.rational import Rational
from abjad.helpers.instances import instances
from copy import copy as python_copy


class _Spanner(object):

   def __init__(self, music):
      #self._receptors = [ ]
      self._leaves = [ ]
      self._extend(instances(music, '_Leaf'))

   ### REPR ###
   
   @property
   def _summary(self):
      if len(self) > 0:
         #return ', '.join([str(x) for x in self.leaves])
         return ', '.join([str(x) for x in self])
      else:
         return ' '

   def __repr__(self):
      try:
         return self.before(self[0])[0]
      except:
         return '%s(%s)' % (self.__class__.__name__, self._summary)

   ### OVERRIDES ###

   def __contains__(self, arg):
      #return arg in self._receptors or arg in self.leaves 
      return arg in self._leaves 

   def __getitem__(self, arg):
#      if isinstance(arg, int):
#         #return self._receptors[arg]
#      elif isinstance(arg, slice):
#         #return self._receptors[arg]
      if isinstance(arg, (int, slice)):
         return self._leaves[arg]
      else:
         raise ValueError('must get int or slice.')

   def __len__(self):
      #return len(self._receptors)
      return len(self._leaves)

   def index(self, leaf):
#      try:
#         return self._receptors.index(expr)
#      except:
#         for receptor in self:
#            if receptor._client == expr:
#               return self.index(receptor)
      return self._leaves.index(leaf)

   def _before(self, leaf):
      return [ ]

   def _after(self, leaf):
      return [ ]

   def _left(self, leaf):
      return [ ]

   def _right(self, leaf):
      return [ ]

#   ### CONTENTS TESTING (RECEPTOR) ###
#
#   def _isMyFirstReceptor(self, receptor):
#      return len(self) > 0 and receptor == self[0]
#   
#   def _isMyLastReceptor(self, receptor):
#      return len(self) > 0 and receptor == self[-1]
#
#   def _isMyOnlyReceptor(self, receptor):
#      return self._isMyFirstReceptor(receptor) and \
#         self._isMyLastReceptor(receptor)

   ### CONTENTS TESTING (LEAF) ###

   def _isMyFirstLeaf(self, leaf):
      #return len(self) > 0 and leaf == self.leaves[0]
      return len(self) > 0 and leaf == self[0]
   
   def _isMyLastLeaf(self, leaf):
      #return len(self) > 0 and leaf == self.leaves[-1]
      return len(self) > 0 and leaf == self[-1]

   def _isMyOnlyLeaf(self, leaf):
      return self._isMyFirstLeaf(leaf) and self._isMyLastLeaf(leaf)

   def _isMyFirst(self, leaf, classname):
      if leaf.kind(classname):
         i = self.index(leaf)
         #for x in self.leaves[ : i]:
         for x in self[ : i]:
            if x.kind(classname):
               return False
         return True
      return False

   def _isMyLast(self, leaf, classname):
      if leaf.kind(classname):
         i = self.index(leaf)
         #for x in self.leaves[i + 1 : ]:
         for x in self[i + 1 : ]:
            if x.kind(classname):
               return False
         return True
      return False

   def _isMyOnly(self, leaf, classname):
      return leaf.kind(classname) and len(self) == 1

   ### DERIVED CONTENTS PROPERTIES ###

   def _durationOffsetInMe(self, leaf):
      assert leaf in self
      #prev = self.leaves[ : self.index(leaf)]
      prev = self[ : self.index(leaf)]
      #return sum([leaf.duration.prolated for leaf in prev], Rational(0))
      return sum([leaf.duration.prolated for leaf in prev])

   ### RECEPTOR INSERTS ###

   def _insert(self, i, l):
      l.spanners._spanners.append(self)
      #self._receptors.insert(i, l.spanners)
      self._leaves.insert(i, l)

   def _append(self, l):
      self._insert(len(self), l)

   def _extend(self, leaves):
      for l in leaves:
         self._append(l)

#   ### DEPRECATED RECEPTOR-ONLY REFERENCE MANAGEMENT ###
#
#   def _blockByReference(self, receptor):
#      receptor._spanners.remove(self)
#
#   def _block(self, i = None, j = None):
#      if i is not None and j is None:
#         receptor = self[i]
#         self._blockByReference(receptor)
#      elif i is not None and j is not None:
#         for receptor in self[i : j + 1]:
#            self._blockByReference(receptor)
#      else:
#         for receptor in self:
#            self._blockByReference(receptor)
#
#   def _unblockByReference(self, receptor):
#      if self not in receptor:
#         receptor.append(self)
#
#   def _unblock(self, i = None, j = None):
#      if i is not None and j is None:
#         receptor = self[i]
#         self._unblockByReference(receptor)
#      elif i is not None and j is not None:
#         for receptor in self[i : j + 1]:
#            self._unblockByReference(receptor)
#      else:
#         for receptor in self:
#            self._unblockByReference(receptor)
#
#   def _removeByReference(self, receptor):
#      self._receptors.remove(receptor)
#
#   def _remove(self, i = None, j = None):
#      if i is not None and j is None:
#         self._removeByReference(self[i])
#      elif i is not None and j is not None:
#         for receptor in self[i : j + 1]:
#            self._removeByReference(receptor)
#      else:
#         for receptor in self[ : ]:
#            self._removeByReference(receptor)
#            print self._receptors
#
#   def _severByReference(self, receptor):
#      self._blockByReference(receptor)
#      self._removeByReference(receptor)
#
#   def _sever(self, i = None, j = None):
#      if i is not None and j is None:
#         receptor = self[i]
#         self._severByReference(receptor)
#      elif i is not None and j is not None:
#         for n in reversed(range(i, j + 1)):
#            receptor = self[n]
#            self._severByReference(receptor)
#      else:
#         for n in reversed(range(len(self))):
#            receptor = self[n]
#            self._severByReference(receptor)
#
#   def die(self):
#      self._sever( )

   ### LEAF-ONLY REFERENCE MANAGEMENT ###

   def _blockByReference(self, leaf):
      leaf.spanners._spanners.remove(self)

   def _block(self, i = None, j = None):
      if i is not None and j is None:
         leaf = self[i]
         self._blockByReference(leaf)
      elif i is not None and j is not None:
         for leaf in self[i : j + 1]:
            self._blockByReference(leaf)
      else:
         for leaf in self:
            self._blockByReference(leaf)

   def _unblockByReference(self, leaf):
      if self not in leaf.spanners:
         leaf.spanners._append(self)

   def _unblock(self, i = None, j = None):
      if i is not None and j is None:
         leaf = self[i]
         self._unblockByReference(leaf)
      elif i is not None and j is not None:
         for leaf in self[i : j + 1]:
            self._unblockByReference(leaf)
      else:
         for leaf in self:
            self._unblockByReference(leaf)

   def _removeByReference(self, leaf):
      self._leaves.remove(leaf)

   def _remove(self, i = None, j = None):
      if i is not None and j is None:
         self._removeByReference(self[i])
      elif i is not None and j is not None:
         for leaf in self[i : j + 1]:
            self._removeByReference(leaf)
      else:
         for leaf in self[ : ]:
            self._removeByReference(leaf)

   def _severByReference(self, leaf):
      self._blockByReference(leaf)
      self._removeByReference(leaf)

   def _sever(self, i = None, j = None):
      if i is not None and j is None:
         leaf = self[i]
         self._severByReference(leaf)
      elif i is not None and j is not None:
         for n in reversed(range(i, j + 1)):
            leaf = self[n]
            self._severByReference(leaf)
      else:
         for n in reversed(range(len(self))):
            leaf = self[n]
            self._severByReference(leaf)

   def die(self):
      self._sever( )

   ### SPANNER TESTING ###

   ### TODO - consider implementing a dedicated attribute comparison method
   ###        to work on any two spanners;
   ###        such a method would feed into _matches( ), below.

   ### TODO - figure out if we really need the attribute check or not;
   ###        looks like the attribute check doesn't work right now,
   ###        at least not for two different octavation spanners.
   def _matches(self, spanner):
      return self.__class__ == spanner.__class__ and \
         all([getattr(self, attr, None) == getattr(spanner, attr, None)
            for attr in ('_grob', '_attribute', '_value')])

   def _follows(self, spanner):
      #return spanner.leaves[-1].next == self.leaves[0]
      return spanner[-1].next == self[0]

   ### TODO - _matchingSpanner( ) functions as a generalization of
   ###        _matchingSpannerBeforeMe( ) and _matchingSpannerAfterMe( );
   ###        cleaner to reimplement _matchingSpanner( ) completely
   ###        independently of those two functions 
   ###        and then eliminate those two functions entirely;
   ###        this will take us from three functions down to only _matchingSpanner( ).
   def _matchingSpanner(self, direction):
      assert direction in ('left', 'right')
      if direction == 'left':
         return self._matchingSpannerBeforeMe( )
      else:
         return self._matchingSpannerAfterMe( )

   def _matchingSpannerBeforeMe(self):
      #if self[0]._client.prev:
      if self[0].prev:
         #matches = self[0]._client.prev.spanners.get(
         matches = self[0].prev.spanners.get(
            interface = getattr(self, '_interface', None),
            grob = getattr(self, '_grob', None),
            attribute = getattr(self, '_attribute', None),
            value = getattr(self, '_vallue', None))
         if matches:
            return matches[0]

   def _matchingSpannerAfterMe(self):
      #if self[-1]._client.next:
      if self[-1].next:
         #matches = self[-1]._client.next.spanners.get(
         matches = self[-1].next.spanners.get(
            interface = getattr(self, '_interface', None),
            grob = getattr(self, '_grob', None),
            attribute = getattr(self, '_attribute', None),
            value = getattr(self, '_vallue', None))
         if matches:
            return matches[0]

   ### SPANNER OPERATIONS ###

   def _fractureLeft(self, i):
      left = self.copy(0, i - 1)
      right = self.copy(i, len(self))
      self._block( )
      return self, left, right

   def _fractureRight(self, i):
      left = self.copy(0, i)
      right = self.copy(i + 1, len(self))
      self._block( )
      return self, left, right

### Crashes on direction = 'both'. Fixed below.
#   def fracture(self, i, direction = 'both'):
#      if direction == 'left':
#         return self._fractureLeft(i)
#      elif direction == 'right':
#         return self._fractureRight(i)
#      elif direction == 'both':
#         result = [ ]
#         result.append(self._fractureLeft(i))
#         result.append(self._fractureRight(i))
#      else:
#         raise ValueError(
#            'direction %s must be left, right or both.' % direction)

   def fracture(self, i, direction = 'both'):
      if i < 0:
         i = len(self) + i
      if direction == 'left':
         return self._fractureLeft(i)
      elif direction == 'right':
         return self._fractureRight(i)
      elif direction == 'both':
         left = self.copy(0, i - 1)
         right = self.copy(i + 1, len(self))
         center = self.copy(i, i)
         self._block( )
         return self, left, center, right
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)

   def _fuseByReference(self, spanner):
      if self._matches(spanner) and spanner._follows(self):
         result = self.copy( )
         #result._extend(spanner.leaves)
         result._extend(spanner)
         self._block( )
         spanner._block( )
         return [(self, spanner, result)]
      else:
         return [ ]

   def _fuseRight(self):
      result = [ ]
      if self._matchingSpannerAfterMe( ):
         result.extend(self._fuseByReference(self._matchingSpannerAfterMe( )))
      return result

   def _fuseLeft(self):
      result = [ ]
      if self._matchingSpannerBeforeMe( ):
         result.extend(self._matchingSpannerBeforeMe( )._fuseByReference(self))
      return result

   def fuse(self, direction = 'both'):
      if direction == 'left':
         return self._fuseLeft( )
      elif direction == 'right':
         return self._fuseRight( )
      elif direction == 'both':
         result = [ ]
         result.append(self._fuseLeft( ))
         result.append(self._fuseRight( ))
         return result
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)
      
   def capture(self, n):
      if n > 0:
         #cur = self.leaves[-1]
         cur = self[-1]
         for i in range(n):
            if cur.next:
               self._append(cur.next)
               cur = cur.next         
            else:
               break
      elif n < 0:
         #cur = self.leaves[0]
         cur = self[0]
         for i in range(abs(n)):
            if cur.prev:
               self._insert(0, cur.prev)
               cur = cur.prev
            else:
               break

   def surrender(self, n):
      '''
      Surrender from the right for positive n;
      surrender from the left for negative n;
      never surrender all references;
      (surrender never equals death).
      '''
      if n > 0:
         for i in range(n):
            if len(self) > 1:
               self._sever(-1)
      elif n < 0:
         for i in range(abs(n)):
            if len(self) > 1:
               self._sever(0)

   def move(self, n):
      '''
      Move right positive n;
      move left for negative n;
      always preserve length of self.
      '''
      #start, stop = self.leaves[0], self.leaves[-1]
      start, stop = self[0], self[-1]
      if n > 0:
         for i in range(n):
            if stop.next:
               self.capture(1)
               self.surrender(-1)
               start, stop = start.next, stop.next
            else:
               break
      elif n < 0:
         for i in range(abs(n)):
            if start.prev:
               self.capture(-1)
               self.surrender(1)      
               start, stop = start.prev, stop.prev
            else:
               break

   ### SPANNER COPYING ###

   def copy(self, start = None, stop = None):
      #from copy import copy
      result = python_copy(self)
      #result._receptors = [ ]
      result._leaves = [ ]
      if stop is not None:
         #for receptor in self[start : stop + 1]:
         for leaf in self[start : stop + 1]:
            #result._receptors.append(receptor)
            result._leaves.append(leaf)
      else:
         #for receptor in self:
         for leaf in self:
            #result._receptors.append(receptor)
            result._leaves.append(leaf)
      result._unblock( )
      return result

   ### DERIVED PROPERTIES ###

   @property
   def duration(self):
      #return sum([l.duration.prolated for l in self.leaves])
      return sum([l.duration.prolated for l in self])
