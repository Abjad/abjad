from abjad.core.initializer import _Initializer
from abjad.helpers.clone_fracture import clone_fracture
from abjad.helpers.transfer_all_attributes import _transfer_all_attributes
from abjad.notehead.notehead import NoteHead


class _NoteInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from abjad.rest.rest import Rest
      from abjad.chord.chord import Chord
      from abjad.note.note import Note
      from abjad.skip.skip import Skip
      client.notehead = None
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if isinstance(args[0], Note):
            note = args[0]
            _Leaf.__init__(client, note.duration.written)
            _transfer_all_attributes(note, client)
         if isinstance(args[0], Rest):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written)
            _transfer_all_attributes(rest, client)
            del client._pitch
         elif isinstance(args[0], Chord):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written)
            # must copy chord BEFORE _transfer_all_attributes
            if len(chord) > 0:
               copy = clone_fracture([chord])[0]
            _transfer_all_attributes(chord, client)
            del client._noteheads
            if len(chord) > 0:
               client.notehead = copy.noteheads[0]
         elif isinstance(args[0], Skip):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written)
            _transfer_all_attributes(skip, client)
      elif len(args) == 2:
         pitch, duration = args
         #print pitch, duration, type(pitch)
         _Leaf.__init__(client, duration)
         client.notehead = pitch
         #client.pitch = pitch
      else:
         raise ValueError('can not initialize note.')
