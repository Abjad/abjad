from abjad.components._Context import _Context
from abjad.tools import lilyfiletools


def _insert_expr_into_lily_file(expr):

   if isinstance(expr, lilyfiletools.LilyFile):
      lily_file = expr
   elif isinstance(expr, _Context):
      lily_file = lilyfiletools.make_basic_lily_file(expr)
      lily_file._is_temporary = True
   else:
      lily_file = lilyfiletools.make_basic_lily_file( )
      score_block = lilyfiletools.ScoreBlock( )
      score_block.append(expr)
      lily_file.append(score_block)
      lily_file.score = score_block
      lily_file._is_temporary = True

   return lily_file
