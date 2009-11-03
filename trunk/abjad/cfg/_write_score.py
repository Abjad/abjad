def _write_score(outfile, scorestring):
   '''Puts LilyPond input `scorestring` inside a '\score{ }' block
   and write it to the `outfile` 'file' object. '''
   scorelines = scorestring.replace('\n', '\n\t')
   outfile.write('\\score{\n\t') 
   outfile.write(scorelines)
   outfile.write('\n}')
