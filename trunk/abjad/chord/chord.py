from formatter import ChordFormatter
from initializer import ChordInitializer
from .. leaf.leaf import Leaf
from .. notehead.notehead import NoteHead
from .. pitch.pitch import Pitch

class Chord(Leaf):

   def __init__(self, *args):
      self.initializer = ChordInitializer(self, Leaf, *args)

   ### REPR ### 

   def __repr__(self):
      return 'Chord(%s, %s)' % (self._summary, self.duration._product)

   def __str__(self):
      return '<%s>%s' % (self._summary, self.duration._product)

   ### OVERRIDES ###

   def __len__(self):
      return len(self._noteheads)

   def __contains__(self, arg):
      if isinstance(arg, (int, float, long)):
         return Pitch(arg) in self.pitches
      elif isinstance(arg, Pitch):
         return arg in self.pitches
      elif isinstance(arg, NoteHead):
         return arg in self.noteheads
      else:
         return False

   def __getitem__(self, i):
      return self._noteheads[i]

   def __setitem__(self, i, arg):
      if isinstance(arg, (int, long, float)):
         self._noteheads[i] = NoteHead(pitch = arg)
      elif isinstance(arg, Pitch):
         self._noteheads[i] = NoteHead(pitch = arg)
      elif isinstance(arg, NoteHead):
         self._noteheads[i] = arg

   def __delitem__(self, i):
      del(self._noteheads[i])

   ### HANDLERS ###

   def insert(self, i, arg):
      if isinstance(arg, (int, float, long)):
         self._noteheads.insert(NoteHead(self, pitch = arg))
      elif isinstance(arg, Pitch):
         self._noteheads.insert(NoteHead(self, pitch = arg))
      elif isinstance(arg, NoteHead):
         arg._client = self
         self._noteheads.insert(arg)
      else:
         print 'Can not insert %s into Chord at %s.' % (arg, i)

   def append(self, arg):
      if isinstance(arg, (int, float, long)):
         self._noteheads.append(NoteHead(self, pitch = arg))
      elif isinstance(arg, Pitch):
         self._noteheads.append(NoteHead(self, pitch = arg))
      elif isinstance(arg, NoteHead):
         arg._client = self
         self._noteheads.append(arg)
      else:
         print 'Can not append %s to Chord.' % arg

   def extend(self, arglist):
      assert isinstance(arglist, list)
      for arg in arglist:
         self.append(arg)

   def pop(self, i = -1):
      return self._noteheads.pop(i)

   def remove(self, notehead):
      self._noteheads.remove(notehead)
   
   ### MANAGED ATTRIBUTES ###

   @apply
   def pitches( ):
      def fget(self):
         result = [ ]
         for notehead in self._noteheads:
            if notehead.pitch:
               result.append(notehead.pitch)   
         return result
      def fset(self, arg):
         assert isinstance(arg, list)
         self._noteheads = [ ]
         for x in arg:
            if isinstance(x, (int, float, long)):
               self._noteheads.append(NoteHead(self, pitch = x))
            elif isinstance(x, Pitch):
               self._noteheads.append(NoteHead(self, pitch = x))
            elif isinstance(x, NoteHead):
               x._client = self
               self._noteheads.append(x)
            else:
               print 'Can not set Chord.pitches = [..., %s, ...].' % arg
               raise ValueError
      return property(**locals( ))

   @apply
   def noteheads( ):
      def fget(self):
         result = [ ]
         for notehead in self._noteheads:
            result.append(notehead)
         return result
      def fset(self, arglist):
         assert isinstance(arg, list)
         self._noteheads = [ ]
         for arg in arglist:
            if isinstance(arg, (int, float, long)):
               self._noteheads.append(NoteHead(self, pitch = arg))
            elif isinstance(arg, Pitch):
               self._noteheads.append(NoteHead(self, pitch = arg))
            elif isinstance(aarg, NoteHead):
               arg._client = self
               self._noteheads.append(arg)
            else:
               print 'Can not set Chord.noteheads = [..., %s, ...].' % arg
               raise ValueError
      return property(**locals( ))

   ### FORMATTING ###

   @property
   def _summary(self):
      return ' '.join([str(x) for x in self._noteheads])
