from abjad.markup import Markup


def _write_footer(outfile, footer):

   assert isinstance(footer, (Markup, str))
   outfile.write('\\paper {\n')
   
   if isinstance(footer, Markup):
      outfile.write('\toddFooterMarkup = %s\n' % footer.format)
      outfile.write('\tevenFooterMarkup = %s\n' % footer.format)
   else:
      outfile.write('\toddFooterMarkup = "%s"\n' % footer)
      outfile.write('\tevenFooterMarkup = "%s"\n' % footer)
   outfile.write('}\n\n')
