def unique(ll):
   '''Return unique elements in list ll;
      recipe from Chris Mora;
      
      Mora == slow. Just use set( ). Sorry, Chris.'''

   #return [x for x in ll if x not in locals( )['_[1]']]
   return list(set(ll))
