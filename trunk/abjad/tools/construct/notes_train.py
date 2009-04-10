from abjad.note.note import Note
from abjad.rational.rational import Rational
from abjad.tools.construct.notes import notes as construct_notes


## This is one of the only uses of 'import blah as'; do we need? ##

def note_train(pitch, written_duration, total_duration, 
   prolation = Rational(1)):
   '''Generate a train of repeating notes, all of the same pitch,
      equal to total duration total_duration,
      each with written duration equal to written_duration,
      under prolation context equal to prolation.
      Fill any remaining duration at the end of the train
      with a series of notes with smaller written duration.
      Set prolation when constructing a note train within
      a nonbinary measure.'''

   prolated_duration = prolation * written_duration 
   current_duration = Rational(0)
   result = [ ]
   while current_duration + prolated_duration <= total_duration:
      result.append(Note(pitch, written_duration))
      current_duration += prolated_duration
   remainder_duration = total_duration - current_duration
   if remainder_duration > Rational(0):
      multiplied_remainder = ~prolation * remainder_duration
      result.extend(construct_notes(pitch, [multiplied_remainder]))
   return result
