def _write_local_includes(outfile, includes):
   if includes:
      for i in includes:
         outfile.write('\\include "%s"\n' % i)
