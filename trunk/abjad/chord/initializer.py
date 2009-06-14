from abjad.chord.formatter import _ChordFormatter
from abjad.core.initializer import _Initializer
from abjad.notehead.interface import _NoteHeadInterface


## NOTE - order of steps must be 
##
##        1. _Leaf.__init__
##        2. Chord.formatter = _ChordFormatter
##        3. _transfer_all_attributes
##
##        to first set Chord.formatter = _LeafFormatter, and
##        only then overwrite Chord.formatter = _ChordFormatter, and
##        only then transfer attributes (if necessary).

class _ChordInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from abjad.chord.chord import Chord
      from abjad.tools.scoretools.transfer_all_attributes import _transfer_all_attributes
      from abjad.note.note import Note
      from abjad.rest.rest import Rest
      #from abjad.skip.skip import Skip
      from abjad.skip import Skip
      from abjad.tools import clone
      client.pitches = [ ]
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if isinstance(args[0], Note):
            note = args[0]
            _Leaf.__init__(client, note.duration.written)
            client._formatter = _ChordFormatter(client)
            # must copy notehead (if required) BEFORE
            # _transfer_all_attributes;
            # otherwise note copy will fail to fracture spanners
            if note.notehead is not None:
               copy = clone.fracture([note])[0]
            _transfer_all_attributes(note, client)
            #del client._notehead
            client._notehead = _NoteHeadInterface(client)
            if note.notehead is not None:
               client.append(copy.notehead)
         if isinstance(args[0], Rest):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written)
            client._formatter = _ChordFormatter(client)
            _transfer_all_attributes(rest, client)
            del client._pitch
         elif isinstance(args[0], Chord):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written)
            client._formatter = _ChordFormatter(client)
            _transfer_all_attributes(chord, client)
         elif isinstance(args[0], Skip):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written)
            client._formatter = _ChordFormatter(client)
            _transfer_all_attributes(skip, client)
      elif len(args) == 2:
         pitches, duration = args
         _Leaf.__init__(client, duration)
         client._formatter = _ChordFormatter(client)
         client.pitches = pitches
      else:
         raise ValueError('can not initialize chord.')
