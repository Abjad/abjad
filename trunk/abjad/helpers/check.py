from abjad import checks as _checks


def check(expr, runtime = 'composition'):
   '''Run every check in the 'check' module against expr.

      Set the 'runtime' keyword to 'composition' to run
      only those checks appropriate at composition-time.
      Abjad allow empty containers at composition-time.
      Empty container checks will NOT run.

      abjad> check(Voice([ ]), runtime = 'composition')
      True

      Set the 'runtime' keyword to 'format' to run the 
      complete set of checks appropriate at format-time.
      LilyPond does NOT allow empty containers at format-time.
      Empty container check WILL run.

      abjad> check(Voice([ ]), runtime = 'format')
      False'''

   results = [ ]
   for key, value in sorted(_checks.__dict__.items( )):
      checker = value( )
      if runtime == 'composition':
         if getattr(checker, 'runtime', False) == 'composition':
            continue
      results.append(checker.check(expr))
   return all(results) 
