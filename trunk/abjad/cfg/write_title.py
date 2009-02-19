def _write_title(outfile, title):
   outfile.write('\\header {\n')
   outfile.write('\ttitle = "%s"\n' % title)
   outfile.write('}\n\n')
