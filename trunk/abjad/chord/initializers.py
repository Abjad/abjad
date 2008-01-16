from .. duration.duration import Duration
from .. note.note import Note
from .. notehead.notehead import NoteHead
from .. pitch.pitch import Pitch

class _ChordInit(object):

   pass

class InitializeDurationByNumeratorDenominator(_ChordInit):

   def matchSignature(self, arg):
      return isinstance(arg, tuple) and \
         len(arg) == 2

   def initialize(self, client, arg):
      client.duration.duratum = Duration(*arg)

class InitializeDurationByDuration(_ChordInit):
   
   def matchSignature(self, arg):
      return isinstance(duration, Duration)

   def initialize(self, client, arg):
      client.duration.duratum = Duration(*arg)

class InitializeNoteHeadsByPitchNumberList(_ChordInit):
   
   def matchSignature(self, arg):
      return isinstance(arg, list) and \
         isinstance(arg[0], (int, long, float))

   def initialize(self, client, arg):
      for p in arg:
         client.noteheads.append(NoteHead(p))

class InitializeNoteHeadsByPitchList(_ChordInit):

   def matchSignature(self, arg):
      return isinstance(arg, list) and \
         isinstance(arg[0], Pitch)

   def initialize(self, client, arg):
      for pitch in arg:
         client.noteheads.append(NoteHead(pitch))

class InitializeNoteHeadByNoteHeadList(_ChordInit):

   def matchSignature(self, arg):
      return isistance(arg, list) and \
         isinstance(arg[0], NoteHead)

   def initialize(self, client, arg):
      for notehead in arg:
         client.noteheads.append(notehead)

class InitializeNoteHeadsByNoteList(_ChordInit):

   def matchSignature(self, arg):
      return isinstance(arg, list) and \
         isinstance(arg[0], Note)

   def initialize(self, client, arg):
      for note in arg:
         client.noteheads.append(NoteHead(note))
