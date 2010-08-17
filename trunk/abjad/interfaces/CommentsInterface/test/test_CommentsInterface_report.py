from abjad import *


def test_CommentsInterface_report_01( ):
   '''Report container comments.'''

   t = Voice(macros.scale(4))
   BeamSpanner(t[:])
   t.comments.before.append('Comments before.')
   t.comments.before.append('More comments before.')
   t.comments.opening.append('Comments opening.')

   r'''
   % Comments before.
   % More comments before.
   \new Voice {
      % Comments opening.
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   result = t.comments.report(output = 'string')

   r'''
   before
      % Comments before.
      % More comments before.
   opening
      % Comments opening.'''

   assert result == 'before\n\t% Comments before.\n\t% More comments before.\nopening\n\t% Comments opening.\n'
