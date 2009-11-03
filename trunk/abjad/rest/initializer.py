from abjad.core.initializer import _Initializer
#from abjad.notehead.interface import NoteHeadInterface
from abjad.interfaces.note_head.interface import NoteHeadInterface


class _RestInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from abjad.chord import Chord
      from abjad.tools.scoretools.transfer_all_attributes import \
         _transfer_all_attributes
      from abjad.note import Note
      from abjad.rest import Rest
      from abjad.skip import Skip
      client.pitch = None
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if isinstance(args[0], Note):
            note = args[0]
            _Leaf.__init__(client, note.duration.written)
            _transfer_all_attributes(note, client)
            #del client._note_head
            client._note_head = NoteHeadInterface(client)
         if isinstance(args[0], Rest):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written)
            _transfer_all_attributes(rest, client)
         elif isinstance(args[0], Chord):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written)
            _transfer_all_attributes(chord, client)
            del client._note_heads
         elif isinstance(args[0], Skip):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written)
            _transfer_all_attributes(skip, client)
      elif len(args) == 1:
         duration = args[0]
         _Leaf.__init__(client, duration)
      else:
         raise ValueError('can not initialize rest.')
