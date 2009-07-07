def _write_title(outfile, title):
   if isinstance(title, str):
      outfile.write('\\header {\n')
      outfile.write('\ttitle = "%s"\n' % title)
      outfile.write('}\n\n')
   elif isinstance(title, list) and title:
      outfile.write('\\header {\n')
      main_line ='"%s"' % title[0]
      secondary_lines = title[1:]
      secondary_lines = [r'\smaller { "%s" }' % x for x in secondary_lines]
      text = [ ]
      text.append(main_line)
      text.extend(secondary_lines)
      text = ' '.join(text)
      markup = r'\markup \column \halign #center { %s }' % text
      outfile.write('\ttitle = %s\n' % markup)
      outfile.write('}\n\n')
