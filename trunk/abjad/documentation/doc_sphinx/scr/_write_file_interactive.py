
def _write_file_interactive(content, file):
   msg = 'Will write file "%s". Proceed? [Y/n]:' % file
   input = raw_input(msg)
   if input.lower( ) in ('y', ''):
      listing_file = open(file, 'w')
      listing_file.write(content)
      listing_file.close( )
