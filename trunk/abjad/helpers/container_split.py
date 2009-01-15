
def container_split(container, index):
   '''
   Splits container in two at given index position.
   '''
   if index == 0 or index > len(container):
      return [container, None]
   c1 = container
   c2 = container.copy( )
   del(c1[index:])
   del(c2[0:index])
   if container._parent:
      container._parent[index:index] = [c2]
   return [c1, c2]
