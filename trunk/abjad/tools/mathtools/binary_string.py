def binary_string(n):
   '''Return the base-2 representation of integer n as a string.
   
      mathtools.binary_string(1) == '1'
      mathtools.binary_string(2) == '10'
      mathtools.binary_string(3) == '11'
      mathtools.binary_string(4) == '100' '''

   result = ''
   while n > 0:
      result = str(n % 2) + result
      n = n >> 1

   return result
