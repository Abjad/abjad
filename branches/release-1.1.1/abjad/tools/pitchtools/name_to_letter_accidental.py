def name_to_letter_accidental(name):
   if len(name) == 1:
      return name, ''
   else:
      return name[0], name[1:]
