#from abjad.note import Note
#from abjad.tools import durtools
#from abjad.tools import scoretools
#from abjad.tools import tietools
#from abjad.tuplet import FixedDurationTuplet
#
#
#def tie_chain(chain, divisions = 2, prolation = 'diminution'):
#   '''Generalization of divide.leaf( ) function.'''
#
#   # find target duration of fixed-duration tuplet
#   target_duration = tietools.get_duration_preprolated(chain[0].tie.chain)
#
#   # find prolated duration of each note in tuplet
#   prolated_duration = target_duration / divisions
#
#   # find written duration of each notes in tuplet
#   if prolation == 'diminution':
#      #written_duration = durtools.prolated_to_written_not_less_than(
#      #   prolated_duration)
#      written_duration = durtools.naive_prolated_to_written_not_less_than(
#         prolated_duration)
#   elif prolation == 'augmentation':
#      #written_duration = durtools.prolated_to_written_not_greater_than(
#      #   prolated_duration)
#      written_duration = durtools.naive_prolated_to_written_not_greater_than(
#         prolated_duration)
#   else:
#      raise ValueError('must be diminution or augmentation.')
#   
#   # make tuplet notes
#   notes = Note(0, written_duration) * divisions
#
#   # make tuplet
#   tuplet = FixedDurationTuplet(target_duration, notes)
#
#   # bequeath tie chain position in score structure to tuplet
#   scoretools.bequeath(list(chain), [tuplet])
#
#   # untie tuplet
#   tuplet.tie.unspan( )
#
#   # return tuplet
#   return tuplet
