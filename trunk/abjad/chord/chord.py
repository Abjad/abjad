from abjad.chord.formatter import _ChordFormatter
from abjad.chord.initializer import _ChordInitializer
from abjad.leaf.leaf import _Leaf
from abjad.notehead import NoteHead
#from abjad.pitch.pitch import Pitch


class Chord(_Leaf):

   def __init__(self, *args):
      self._initializer = _ChordInitializer(self, _Leaf, *args)

   ## OVERLOADS ##

   def __contains__(self, arg):
      from abjad.pitch.pitch import Pitch
      if isinstance(arg, (int, float, long)):
         return Pitch(arg) in self.pitches
      elif isinstance(arg, Pitch):
         return arg in self.pitches
      elif isinstance(arg, NoteHead):
         return arg in self.noteheads
      else:
         return False

   def __delitem__(self, i):
      del(self._noteheads[i])

   def __getitem__(self, i):
      return self._noteheads[i]

   def __len__(self):
      return len(self._noteheads)

   def __repr__(self):
      return 'Chord(%s, %s)' % (self._summary, self.duration._product)

   def __setitem__(self, i, arg):
      from abjad.pitch.pitch import Pitch
      if isinstance(arg, (int, long, float)):
         self._noteheads[i] = NoteHead(self, pitch = arg)
      elif isinstance(arg, Pitch):
         self._noteheads[i] = NoteHead(self, pitch = arg)
      elif isinstance(arg, NoteHead):
         self._noteheads[i] = arg
      self._sort( )

   def __str__(self):
      return '<%s>%s' % (self._summary, self.duration._product)

   ## PRIVATE METHODS ##

   def _sort(self):
      '''Sort noteheads in self by pitch altitude.'''
      def _helper(nh1, nh2):
         altitude_cmp = cmp(nh1.pitch.altitude, nh2.pitch.altitude)
         if altitude_cmp == 0:
            return cmp(nh1.pitch.number, nh2.pitch.number)
         else:
            return altitude_cmp
      self._noteheads.sort(_helper)

   @property
   def _summary(self):
      '''Return string summary of noteheads in self.'''
      return ' '.join([str(x) for x in self._noteheads])

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
   def noteheads( ):
      def fget(self):
         '''Set noteheads from any iterable.
            Get immutable tuple of noteheads in chord.'''
         result = [ ]
         for notehead in self._noteheads:
            result.append(notehead)
         return tuple(result)
      def fset(self, arglist):
         assert isinstance(arglist, (list, tuple, set))
         self._noteheads = [ ]
         for arg in arglist:
            notehead = NoteHead(self, pitch = arg)
            self._noteheads.append(notehead)
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
         for notehead in self._noteheads:
            if notehead.pitch:
               result.append(notehead.pitch)   
         return tuple(result)
      def fset(self, arglist):
         self.noteheads = arglist
      return property(**locals( ))

   ## PUBLIC METHODS ## 

   def append(self, arg):
      '''Append notehead token to self. Then sort noteheads.'''
      from abjad.pitch.pitch import Pitch
      if isinstance(arg, (int, float, long)):
         self._noteheads.append(NoteHead(self, pitch = arg))
      elif isinstance(arg, Pitch):
         self._noteheads.append(NoteHead(self, pitch = arg))
      elif isinstance(arg, NoteHead):
         self._noteheads.append(arg)
      else:
         print 'Can not append %s to Chord.' % arg
      self._sort( )

   def extend(self, arglist):
      '''Extend notehead tokens to self. Then sort noteheads.'''
      assert isinstance(arglist, list)
      for arg in arglist:
         self.append(arg)
      self._sort( )

   def pop(self, i = -1):
      '''Remove last notehead in self. Then return.'''
      notehead = self._noteheads.pop(i)
      notehead._client = None
      return notehead

   def remove(self, notehead):
      '''Remove last notehead in self. Do not return.'''
      notehead._client = None
      self._noteheads.remove(notehead)
