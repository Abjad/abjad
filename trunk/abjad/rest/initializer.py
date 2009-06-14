from abjad.core.initializer import _Initializer
from abjad.notehead.interface import _NoteHeadInterface


class _RestInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from abjad.chord.chord import Chord
      from abjad.tools.scoretools.transfer_all_attributes import _transfer_all_attributes
      from abjad.note.note import Note
      from abjad.rest.rest import Rest
      #from abjad.skip.skip import Skip
      from abjad.skip import Skip
      client.pitch = None
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if isinstance(args[0], Note):
            note = args[0]
            _Leaf.__init__(client, note.duration.written)
            _transfer_all_attributes(note, client)
            #del client._notehead
            client._notehead = _NoteHeadInterface(client)
         if isinstance(args[0], Rest):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written)
            _transfer_all_attributes(rest, client)
         elif isinstance(args[0], Chord):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written)
            _transfer_all_attributes(chord, client)
            del client._noteheads
         elif isinstance(args[0], Skip):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written)
            _transfer_all_attributes(skip, client)
      elif len(args) == 1:
         duration = args[0]
         _Leaf.__init__(client, duration)
      else:
         raise ValueError('can not initialize rest.')
