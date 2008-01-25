from formatter import ChordFormatter
from .. core.initializer import _Initializer
from .. helpers.attributes import transfer_all_attributes

### NOTE - order of steps must be 
###
###        1. Leaf.__init__
###        2. Chord.formatter = ChordFormatter
###        3. transfer_all_attributes
###
###        to first set Chord.formatter = LeafFormatter, and
###        only then overwrite Chord.formatter = ChordFormatter, and
###        only then transfer attributes (if necessary).

class ChordInitializer(_Initializer):
   
   def __init__(self, client, Leaf, *args): 
      from .. note.note import Note
      from .. rest.rest import Rest
      from .. skip.skip import Skip
      client.pitches = [ ]
      if len(args) == 0:
         Leaf.__init__(client, None, None)
         client.formatter = ChordFormatter(client)
      elif len(args) == 1 and isinstance(args[0], Leaf):
         if args[0].kind('Note'):
            note = args[0]
            Leaf.__init__(client, None, None)
            client.formatter = ChordFormatter(client)
            transfer_all_attributes(note, client)
            del client._notehead
            if note.notehead != None:
               copy = note.copy( )
               client.append(copy.notehead)
         if args[0].kind('Rest'):
            rest = args[0]
            Leaf.__init__(client, None, None)
            client.formatter = ChordFormatter(client)
            transfer_all_attributes(rest, client)
            del client._pitch
         elif args[0].kind('Chord'):
            chord = args[0]
            Leaf.__init__(client, None, None)
            client.formatter = ChordFormatter(client)
            transfer_all_attributes(chord, client)
         elif args[0].kind('Skip'):
            skip = args[0]
            Leaf.__init__(client, None, None)
            client.formatter = ChordFormatter(client)
            transfer_all_attributes(skip, client)
      elif len(args) == 1:
         Leaf.__init__(client, None, None)
         client.formatter = ChordFormatter(client)
         pitches = args[0]
         client.pitches = pitches
      elif len(args) == 2:
         pitches, duration = args
         Leaf.__init__(client, duration, None)
         client.formatter = ChordFormatter(client)
         client.pitches = pitches
      elif len(args) == 3:
         pitches, duration, multiplier = args
         Leaf.__init__(client, duration, multiplier)
         client.formatter = ChordFormatter(client)
         client.pitches = pitches
      else:
         raise ValueError('can not initialize chord.')
