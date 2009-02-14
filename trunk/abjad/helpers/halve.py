import math


def halve(n, bigger = 'left', even = 'allowed'):
   '''
   >>> halve(7)
   (4, 3)
   >>> halve(7, bigger = 'right')
   (3, 4)

   >>> halve(8)    
   (4, 4)
   >>> halve(8, bigger = 'left')
   (4, 4)
   >>> halve(8, bigger = 'right')
   (4, 4)
   >>> halve(8, bigger = 'left', even = 'disallowed')
   (5, 3)
   >>> halve(8, bigger = 'right', even = 'disallowed')
   (3, 5)
   ''' 

   smallerHalf = int(math.floor(n / 2))
   biggerHalf = n - smallerHalf

   if (smallerHalf == biggerHalf) and (even != 'allowed'):
      smallerHalf -= 1
      biggerHalf += 1

   if bigger == 'left':
      return (biggerHalf, smallerHalf)
   else:
      return (smallerHalf, biggerHalf)
