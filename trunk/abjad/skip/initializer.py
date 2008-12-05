from abjad.core.initializer import _Initializer
from abjad.helpers.attributes import _transfer_all_attributes


class _SkipInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from abjad.note.note import Note
      from abjad.rest.rest import Rest
      from abjad.chord.chord import Chord
#      if len(args) == 0:
#         _Leaf.__init__(client, None, None)
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if args[0].kind('Note'):
            note = args[0]
            _Leaf.__init__(client, note.duration.written.pair)
            _transfer_all_attributes(note, client)
            del client._notehead
         if args[0].kind('Rest'):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written.pair)
            _transfer_all_attributes(rest, client)
            del client._pitch
         elif args[0].kind('Chord'):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written.pair)
            _transfer_all_attributes(chord, client)
            del client._noteheads
         elif args[0].kind('Skip'):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written.pair)
            _transfer_all_attributes(skip, client)
      elif len(args) == 1:
         duration = args[0]
         _Leaf.__init__(client, duration)
#      elif len(args) == 2:
#         duration, multiplier = args
#         _Leaf.__init__(client, duration, multiplier)
      else:
         raise ValueError('can not initialize skip.')
