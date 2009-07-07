def _write_config_file(path):
   f = open(path, 'w')
   f.write('DEBUG=False\n')
   f.write('pdfviewer =\n')
   f.write('midiplayer =\n')
   f.close( ) 
