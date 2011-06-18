from abjad.tools import lilyfiletools
from abjad.tools import markuptools
from abjad.tools.iotools._template_name_to_template_path import _template_name_to_template_path


def _insert_expr_into_lily_file(expr, template = None, tagline = False):
   from abjad.tools.contexttools._Context import _Context

   if isinstance(expr, lilyfiletools.LilyFile):
      lily_file = expr
   elif isinstance(expr, _Context):
      lily_file = lilyfiletools.make_basic_lily_file(expr)
      lily_file._is_temporary = True
   else:
      lily_file = lilyfiletools.make_basic_lily_file( )
      score_block = lilyfiletools.ScoreBlock( )
      score_block.append(expr)
      ## NOTE: don't quite understand the logic here. 
      ## why append a score_block and then set the score_block attribute
      ## to the same thing?
      lily_file.append(score_block)
      #lily_file.score = score_block
      lily_file.score_block = score_block
      lily_file._is_temporary = True

   if template is not None:
      template_path = _template_name_to_template_path(template)
      lily_file.file_initial_user_includes.append(template_path)

   if not tagline:
      lily_file.header_block.tagline = markuptools.Markup('""')

   return lily_file
