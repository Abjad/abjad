from abjad.tools.treetools._RedBlackTree import _RedBlackTree
from abjad.tools.treetools._RedBlackNode import _RedBlackNode
from random import randrange, shuffle


tree = None


def drunk(n):

    global tree
    tree = _RedBlackTree( )
    knowns = [ ]

    values = range(n)
    shuffle(values)

    # insert n nodes in random order
    for v in values:
        tree._insert_node(_RedBlackNode(v))
        knowns.append(v)
        knowns.sort( )
        assert knowns == map(lambda x: x.key, tree._sort_nodes_inorder( ))

    # delete a node and then insert a node at random
    for i in range(len(values)):
        r = randrange(len(values))
        node = tree._find_by_key(r)
        tree._delete_node(node)
        tree._insert_node(_RedBlackNode(r))
        assert knowns == map(lambda x: x.key, tree._sort_nodes_inorder( ))
    
    # delete all nodes in random order
    shuffle(values)
    for v in values:
        node = tree._find_by_key(v)
        tree._delete_node(node)
        knowns.pop(knowns.index(v)) 
        knowns.sort( )                   
        assert knowns == map(lambda x: x.key, tree._sort_nodes_inorder( ))

def roll(n):
    global tree
    tree = _RedBlackTree( )
    values = range(n)
    shuffle(values)
    i = 0
    for v in values:
        print 'INSERTING: %s' % v
        tree._insert_node(_RedBlackNode(v))
        print '\n', tree, '\n\n'
        i += 1
        assert i == len(tree._sort_nodes_inorder( ))
    print map(lambda x: x.key, tree._sort_nodes_inorder( ))

def unroll( ):
    global tree
    assert isinstance(tree, _RedBlackTree)
    values = range(len(tree._sort_nodes_inorder( )))
    shuffle(values)
    i = len(values)
    for v in values:
        print 'DELETING: %s' % v
        node = tree._find_by_key(v)
        tree._delete_node(node)
        i -= 1
        assert i == len(tree._sort_nodes_inorder( ))
        print '\n', tree, '\n\n'
