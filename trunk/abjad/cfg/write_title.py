def _write_title(outfile, title):
   if title is not None:
      outfile.write('\\header {\n')
      outfile.write('\ttitle = "%s"\n' % title)
      outfile.write('}\n\n')
