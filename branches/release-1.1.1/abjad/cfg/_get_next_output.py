from abjad.cfg._get_last_output import _get_last_output
from abjad.cfg._warn_almost_full import _warn_almost_full


def _get_next_output( ):
   last_output = _get_last_output( )
   if last_output is None:
      next_number = 0
      next_output = '0000.ly'
   else:
      last_number = int(last_output.split('.')[0])
      next_number = last_number + 1
      next_output = '%04d.ly' % next_number
   if next_number > 9000:
      _warn_almost_full(last_number)
   return next_output
