from ... helpers.instances import instances
from .. tools import _report


def check_pitchless_notes(expr, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(expr, ('Note', 'Chord'))
   total, bad = 0, 0
   for leaf in leaves:
      total += 1
      if leaf.kind('Note'):
         if leaf.pitch is None or leaf.pitch.number is None:
            violators.append(leaf)
      elif leaf.kind('Chord'):
         if leaf.pitches is None or leaf.pitches == [ ]:
            violators.append(leaf)
   msg = 'notes or chords without pitch.'
   return _report(report, ret, violators, len(leaves), msg)
