
def _write_file_interactive(content, file):
   msg = 'Will write file "%s". Proceed? [y/n]:' % file
   input = raw_input(msg)
   if input.lower( ) == 'y':
      listing_file = open(file, 'w')
      listing_file.write(content)
      listing_file.close( )
