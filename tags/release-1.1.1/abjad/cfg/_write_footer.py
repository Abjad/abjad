from abjad.markup import Markup
import types


def _write_footer(outfile, footer):

   assert isinstance(footer, (Markup, str, types.NoneType))
   outfile.write('\\paper {\n')
   
   if isinstance(footer, Markup):
      outfile.write('\toddFooterMarkup = %s\n' % footer.format)
      outfile.write('\tevenFooterMarkup = %s\n' % footer.format)
   elif isinstance(footer, str):
      outfile.write('\toddFooterMarkup = "%s"\n' % footer)
      outfile.write('\tevenFooterMarkup = "%s"\n' % footer)
   elif isinstance(footer, types.NoneType):
      pass
   outfile.write('}\n\n')
