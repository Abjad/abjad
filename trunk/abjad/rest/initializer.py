from .. core.initializer import _Initializer
from .. helpers.attributes import transfer_all_attributes

class RestInitializer(_Initializer):
   
   def __init__(self, client, Leaf, *args): 
      from .. note.note import Note
      from .. chord.chord import Chord
      from .. skip.skip import Skip

      client.pitch = None

#      if len(args) == 0:
#         Leaf.__init__(client, None, None)
      if len(args) == 1 and isinstance(args[0], Leaf):
         if args[0].kind('Note'):
            note = args[0]
            Leaf.__init__(client, note.duration.written.pair)
            transfer_all_attributes(note, client)
            del client._notehead
         if args[0].kind('Rest'):
            rest = args[0]
            Leaf.__init__(client, rest.duration.written.pair)
            transfer_all_attributes(rest, client)
         elif args[0].kind('Chord'):
            chord = args[0]
            Leaf.__init__(client, chord.duration.written.pair)
            transfer_all_attributes(chord, client)
            del client._noteheads
         elif args[0].kind('Skip'):
            skip = args[0]
            Leaf.__init__(client, skip.duration.written.pair)
            transfer_all_attributes(skip, client)
      elif len(args) == 1:
         duration = args[0]
         Leaf.__init__(client, duration)
         #client.duration = duration
#      elif len(args) == 2:
#         duration, multiplier = args
#         Leaf.__init__(client, duration, multiplier)
      else:
         raise ValueError('can not initialize rest.')
