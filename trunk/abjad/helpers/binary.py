def binary(n):
   result = ''
   while n > 0:
      result = str(n % 2) + result
      n = n >> 1
   return result
