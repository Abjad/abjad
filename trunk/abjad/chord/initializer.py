from formatter import _ChordFormatter
from .. core.initializer import _Initializer
from .. helpers.attributes import _transfer_all_attributes

### NOTE - order of steps must be 
###
###        1. _Leaf.__init__
###        2. Chord.formatter = _ChordFormatter
###        3. _transfer_all_attributes
###
###        to first set Chord.formatter = _LeafFormatter, and
###        only then overwrite Chord.formatter = _ChordFormatter, and
###        only then transfer attributes (if necessary).

class _ChordInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from .. note.note import Note
      from .. rest.rest import Rest
      from .. skip.skip import Skip
      client.pitches = [ ]
#      if len(args) == 0:
#         _Leaf.__init__(client, None, None)
#         client.formatter = _ChordFormatter(client)
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if args[0].kind('Note'):
            note = args[0]
            _Leaf.__init__(client, note.duration.written.pair)
            client.formatter = _ChordFormatter(client)
            _transfer_all_attributes(note, client)
            del client._notehead
            if note.notehead != None:
               copy = note.copy( )
               client.append(copy.notehead)
         if args[0].kind('Rest'):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written.pair)
            client.formatter = _ChordFormatter(client)
            _transfer_all_attributes(rest, client)
            del client._pitch
         elif args[0].kind('Chord'):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written.pair)
            client.formatter = _ChordFormatter(client)
            _transfer_all_attributes(chord, client)
         elif args[0].kind('Skip'):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written.pair)
            client.formatter = _ChordFormatter(client)
            _transfer_all_attributes(skip, client)
#      elif len(args) == 1:
#         _Leaf.__init__(client, None, None)
#         client.formatter = _ChordFormatter(client)
#         pitches = args[0]
#         client.pitches = pitches
      elif len(args) == 2:
         pitches, duration = args
         _Leaf.__init__(client, duration)
         client.formatter = _ChordFormatter(client)
         client.pitches = pitches
#      elif len(args) == 3:
#         pitches, duration, multiplier = args
#         _Leaf.__init__(client, duration, multiplier)
#         client.formatter = _ChordFormatter(client)
#         client.pitches = pitches
      else:
         raise ValueError('can not initialize chord.')
