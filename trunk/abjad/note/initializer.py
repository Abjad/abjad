from abjad.core.initializer import _Initializer
from abjad.helpers.attributes import _transfer_all_attributes


class _NoteInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from abjad.rest.rest import Rest
      from abjad.chord.chord import Chord
      from abjad.skip.skip import Skip

      client.notehead = None
      #if len(args) == 0:
      #   _Leaf.__init__(client, None, None)
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if args[0].kind('Note'):
            note = args[0]
            _Leaf.__init__(client, note.duration.written.pair)
            _transfer_all_attributes(note, client)
         if args[0].kind('Rest'):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written.pair)
            _transfer_all_attributes(rest, client)
            del client._pitch
         elif args[0].kind('Chord'):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written.pair)
            # must copy chord BEFORE _transfer_all_attributes
            if len(chord) > 0:
               copy = chord.copy( )
            _transfer_all_attributes(chord, client)
            del client._noteheads
            if len(chord) > 0:
               #copy = chord.copy()
               client.notehead = copy.noteheads[0]
         elif args[0].kind('Skip'):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written.pair)
            _transfer_all_attributes(skip, client)
#      elif len(args) == 1:
#         _Leaf.__init__(client, None, None)
#         pitch = args[0]
#         client.pitch = pitch
      elif len(args) == 2:
         pitch, duration = args
         _Leaf.__init__(client, duration)
         client.pitch = pitch
#      elif len(args) == 3:
#         pitch, duration, multiplier = args
#         _Leaf.__init__(client, duration, multiplier)
#         client.pitch = pitch
      else:
         raise ValueError('can not initialize note.')
