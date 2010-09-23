def _write_score(outfile, scorestring):
   '''Put LilyPond `scorestring` inside a score block and write it to `outfile`.
   '''

   scorelines = scorestring.replace('\n', '\n\t')
   outfile.write('\\score{\n\t') 
   outfile.write(scorelines)
   outfile.write('\n}')
