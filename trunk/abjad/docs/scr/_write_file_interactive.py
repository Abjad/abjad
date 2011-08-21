def _write_file_interactive(content, file, interactive):
   if interactive.lower in ('y', ''):
      msg = 'Will write file "%s". Proceed? [Y/n]:' % file
      input = raw_input(msg)
   else:
      input = 'Y'
   if input.lower() in ('y', ''):
      #print 'Writing file %s ...' % file
      # if file already exists,
      # do not overwrite unless content has changed.
      try:
         prev_file = open(file, 'r')
         prev_content = prev_file.read()
         prev_file.close()
         if content != prev_content:
            listing_file = open(file, 'w')
            listing_file.write(content)
            listing_file.close()
      except:
         listing_file = open(file, 'w')
         listing_file.write(content)
         listing_file.close()
