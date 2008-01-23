import checks


def check(expr, report = True, ret = None,
   grob = None, attribute = None, value = None):
   result = [ ]
   for name in dir(checks):
      if name.startswith('check_'):
         test = checks.__dict__[name]
         result.append(test(expr, report = report, ret = ret,
            grob = grob, attribute = attribute, value = value))

   if ret == 'violators':
      new = [ ]
      for sublist in result:
         new.extend(sublist)
      return new
   else:
      return all(result)
