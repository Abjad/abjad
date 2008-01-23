import checks


def check(expr, report = True, ret = None):
   result = [ ]
   for name in dir(checks):
      if name.startswith('check_'):
         test = checks.__dict__[name]
         result.append(test(expr, report = report, ret = ret))
   if ret == 'violators':
      new = [ ]
      for sublist in result:
         new.extend(sublist)
      return new
   elif ret:
      return all(result)
   else:
      return None
