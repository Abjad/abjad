from abjad.cfg.cfg import ABJADPATH
import os


def _write_layout_template(outfile, template):
   if template:
      TEMPLATESDIR = ABJADPATH + 'templates/'
      names  = [template, template + '.ly']
      names += [TEMPLATESDIR + template, TEMPLATESDIR + template + '.ly']
      found = False
      for name in names:
         try:
            os.stat(name)
            outfile.write(r'\include "%s"' % name)
            outfile.write('\n')
            break
         except OSError:
            pass
      else:
         print 'WARNING: can not find %s template.' % template         
