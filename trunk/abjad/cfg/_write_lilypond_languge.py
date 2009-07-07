from abjad.cfg.cfg import LILYPONDLANG


def _write_lilypond_language(outfile):
   outfile.write(r'\include "%s.ly"' % LILYPONDLANG.lower( ))
   outfile.write('\n')
