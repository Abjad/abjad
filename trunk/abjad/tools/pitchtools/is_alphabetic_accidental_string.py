import re


alphabetic_accidental_regex_body = """
   ([s]{1,2}    ## s or ss for sharp or double sharp
   |[f]{1,2}    ## or f or ff for flat or double flat
   |t?q?[fs]   ## or qs, qf, tqs, tqf for quartertone accidentals
   |            ## or empty string for no natural
   )!?          ## plus optional ! for forced printing of accidental
   """

alphabetic_accidental_regex = re.compile('^%s$' % 
   alphabetic_accidental_regex_body, re.VERBOSE)

def is_alphabetic_accidental_string(expr):
   '''True when `expr` has the form of an accidental alphabetic string::

      abjad> pitchtools.is_alphabetic_accidental_string('tqs!')
      True

   False otherwise::

      abjad> pitchtools.is_diatonic_pitch_class_name_string('foo')
      False

   The regex ``^([s]{1,2}|[f]{1,2}|t?q?[fs])!?$`` underlies the predicate.
   '''

   return bool(alphabetic_accidental_regex.match(expr))
