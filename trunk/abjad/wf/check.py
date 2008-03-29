import checks


def check(expr, report = True, ret = None):
   result = [ ]
   for key, value in sorted(checks.__dict__.iteritems( )):
      result.append(value(expr, report = report, ret = ret))
   if ret == 'violators':
      new = [ ]
      for sublist in result:
         new.extend(sublist)
      return new
   elif ret:
      return all(result)
   else:
      return None
