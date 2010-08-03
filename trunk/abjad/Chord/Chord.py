from abjad.Chord.formatter import _ChordFormatter
from abjad.Chord.initializer import _ChordInitializer
from abjad._Leaf import _Leaf
from abjad.NoteHead import NoteHead
from abjad.Pitch import Pitch


class Chord(_Leaf):

   def __init__(self, *args):
      self._initializer = _ChordInitializer(self, _Leaf, *args)

   ## OVERLOADS ##

   def __contains__(self, arg):
      if isinstance(arg, (int, float, long)):
         return Pitch(arg) in self.pitches
      elif isinstance(arg, Pitch):
         return arg in self.pitches
      elif isinstance(arg, NoteHead):
         return arg in self.note_heads
      else:
         return False

   def __delitem__(self, i):
      del(self._note_heads[i])

   def __getitem__(self, i):
      return self._note_heads[i]

   def __len__(self):
      return len(self._note_heads)

   def __repr__(self):
      return 'Chord(%s, %s)' % (self._summary, self.duration)

   def __setitem__(self, i, arg):
      if isinstance(arg, (int, long, float)):
         self._note_heads[i] = NoteHead(self, pitch = arg)
      elif isinstance(arg, Pitch):
         self._note_heads[i] = NoteHead(self, pitch = arg)
      elif isinstance(arg, NoteHead):
         self._note_heads[i] = arg
         arg._client = self
      self._sort( )

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_representation(self):
      return '<%s>%s' % (self._summary, self.duration)

   ## PRIVATE METHODS ##

   def _sort(self):
      '''Sort note_heads in self by pitch altitude.'''
      def _helper(nh1, nh2):
         altitude_cmp = cmp(nh1.pitch.altitude, nh2.pitch.altitude)
         if altitude_cmp == 0:
            return cmp(nh1.pitch.number, nh2.pitch.number)
         else:
            return altitude_cmp
      self._note_heads.sort(_helper)

   @property
   def _summary(self):
      '''Return string summary of note_heads in self.'''
      return ' '.join([str(x) for x in self._note_heads])

   ## PUBLIC ATTRIBUTES ## 

   @property
   def center(self):
      '''Return arithmetic mean of pitch numbers in self.'''
      numbers = self.numbers
      if numbers:
         return sum(numbers).__truediv__(len(numbers))
      else:
         return None

   @apply
   def note_heads( ):
      def fget(self):
         '''Set note_heads from any iterable.
            Get immutable tuple of note_heads in chord.'''
         result = [ ]
         for note_head in self._note_heads:
            result.append(note_head)
         return tuple(result)
      def fset(self, arglist):
         assert isinstance(arglist, (list, tuple, set, str))
         self._note_heads = [ ]
         if isinstance(arglist, str):
            arglist = arglist.split( )
         for arg in arglist:
            note_head = NoteHead(self, pitch = arg)
            self._note_heads.append(note_head)
         self._sort( )
      return property(**locals( ))

   @property
   def numbers(self):
      '''Return sorted immutable tuple of pitch numbers in self.'''
      return tuple([pitch.number for pitch in self.pitches])

   @property
   def pairs(self):
      '''Return sorted immutable tuple of pitch pairs in self.'''
      return tuple([pitch.pair for pitch in self.pitches])

   @apply
   def pitches( ):
      def fget(self):
         '''Return immutable tuple of pitches in self.'''
         result = [ ]
         for note_head in self._note_heads:
            if note_head.pitch:
               result.append(note_head.pitch)   
         return tuple(result)
      def fset(self, arglist):
         self.note_heads = arglist
      return property(**locals( ))

   ## PUBLIC METHODS ## 

   def append(self, arg):
      '''Append note_head token to self. Then sort note_heads.'''
      if isinstance(arg, (int, float, long)):
         self._note_heads.append(NoteHead(self, pitch = arg))
      elif isinstance(arg, Pitch):
         self._note_heads.append(NoteHead(self, pitch = arg))
      elif isinstance(arg, NoteHead):
         self._note_heads.append(arg)
         arg._client = self
      else:
         print 'Can not append %s to Chord.' % arg
      self._sort( )

   def extend(self, arglist):
      '''Extend note_head tokens to self. Then sort note_heads.'''
      assert isinstance(arglist, (tuple, list))
      for arg in arglist:
         self.append(arg)
      self._sort( )

   def pop(self, i = -1):
      '''Remove last note_head in self. Then return.'''
      note_head = self._note_heads.pop(i)
      note_head._client = None
      return note_head

   def remove(self, note_head):
      '''Remove last note_head in self. Do not return.'''
      note_head._client = None
      self._note_heads.remove(note_head)
