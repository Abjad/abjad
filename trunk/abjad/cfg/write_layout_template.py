from abjad.cfg.cfg import ABJADTEMPLATES
import os


def _write_layout_template(outfile, template):
   if template:
      names = [template, template + '.ly']
      if ABJADTEMPLATES is not None:
         for path in ABJADTEMPLATES.split(':'):
            names.append(path + os.sep + template)
            names.append(path + os.sep + template + '.ly')
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
