from abjad.cfg.cfg import LILYPONDINCLUDES


def _write_environment_includes(outfile):
   if LILYPONDINCLUDES is not None:
      includes = LILYPONDINCLUDES.split(':')
      for i in includes:
         outfile.write('\\include "%s"\n' % i)
