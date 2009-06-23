def _write_file_interactive(content, file, interactive):
   if interactive.lower in ('y', ''):
      msg = 'Will write file "%s". Proceed? [Y/n]:' % file
      input = raw_input(msg)
   else:
      input = 'Y'
   if input.lower( ) in ('y', ''):
      print 'Writing file %s ...' % file
      listing_file = open(file, 'w')
      listing_file.write(content)
      listing_file.close( )
