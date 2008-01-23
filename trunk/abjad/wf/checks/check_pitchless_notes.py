

def check_pitchless_notes(self, report = True, ret = 'violators'):
   violators = [ ]
   leaves = instances(self._target, ('Note', 'Chord'))
   total, bad = 0, 0
   for leaf in leaves:
      total += 1
      if leaf.kind('Note'):
         if leaf.pitch is None or leaf.pitch.number is None:
            bad += 1
      elif leaf.kind('Chord'):
         if leaf.pitches is None or leaf.pitches == [ ]:
            bad += 1
   if report:
      print '%4d / %4d notes or chords without pitch.' % (bad, total)
   if ret == 'violators':
      return violators
   elif ret:
      return bad == 0
   else:
      return None
