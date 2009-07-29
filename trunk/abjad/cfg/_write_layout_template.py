#from abjad.cfg.cfg import ABJADTEMPLATES
from abjad.cfg._read_config_file import _read_config_file
import os


def _write_layout_template(outfile, template):
   ABJADTEMPLATES = _read_config_file( )['abjad_templates']
   if template:
      names = [template, template + '.ly']
      if ABJADTEMPLATES is not None:
         for path in ABJADTEMPLATES:
            names.append(os.path.join(path, template))
            names.append(os.path.join(path, template + '.ly'))
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
