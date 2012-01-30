from abjad.tools.intervaltreetools._RedBlackNode import _RedBlackNode


class _RedBlackTree(object):

    __slots__ = ('_root', '_sentinel')

    def __init__(self):
        self._sentinel = _RedBlackNode()
        self._sentinel.red = True
        self._sentinel.left = self._sentinel
        self._sentinel.right = self._sentinel
        self._sentinel.parent = self._sentinel
        self._root = self._sentinel

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % (type(self).__name__)

    def __str__(self):
        if self._root == self._sentinel: return '<empty tree>'
        def recurse(node):
            if node == self._sentinel: return [], 0, 0
            if node.red:
                color = 'r'
            else:
                color = 'b'
            label = '%s%s' % (node.key, color)
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
                node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                ' ' * left_pos + '/' + ' ' * (middle-2) +
                '\\' + ' ' * (right_width - right_pos)] + \
                [left_line + ' ' * (width - left_width - right_width) +
                right_line
                for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width
        return '\n'.join(recurse(self._root) [0])

    ### PRIVATE METHODS ###

    def _delete_fixup(self, x):
        while x != self._root and not x.red:
            if x == x.parent.left:
                w = x.parent.right
                # case one
                if w.red:
                    w.red = False
                    x.parent.red = True
                    if x.parent.right != self._sentinel:
                        self._rotate_left(x.parent)
                        w = x.parent.right
                # case two
                if not w.left.red and not w.right.red:
                    w.red = True
                    x = x.parent
                else:
                    # case three
                    if not w.right.red:
                        w.left.red = False
                        w.red = True
                        if w.left != self._sentinel:
                            self._rotate_right(w)
                            w = x.parent.right
                    # case four
                    w.red = x.parent.red
                    x.parent.red = False
                    w.right.red = False
                    if x.parent != self._sentinel:
                        self._rotate_left(x.parent)
                    x = self._root
            else:
                w = x.parent.left
                # case one
                if w.red:
                    w.red = False
                    x.parent.red = True
                    if x.parent.left != self._sentinel:
                        self._rotate_right(x.parent)
                        w = x.parent.left
                # case two
                if not w.right.red and not w.left.red:
                    w.red = True
                    x = x.parent
                else:
                    # case three
                    if not w.left.red:
                        w.right.red = False
                        w.red = True
                        if w.right != self._sentinel:
                            self._rotate_left(w)
                            w = x.parent.left
                    # case four
                    w.red = x.parent.red
                    x.parent.red = False
                    w.left.red = False
                    if x.parent != self._sentinel:
                        self._rotate_right(x.parent)
                    x = self._root
        x.red = False

    def _delete_node(self, z):
        if z.left == self._sentinel or z.right == self._sentinel:
            y = z
        else:
            y = self._find_successor(z)

        if y.left != self._sentinel:
            x = y.left
        else:
            x = y.right

        x.parent = y.parent

        if y.parent == self._sentinel:
            self._root = x
        elif y.is_left_child:
            y.parent.left = x
        else:
            y.parent.right = x

        if y != z:
            z.key = y.key
            z.payload = y.payload

        if not y.red:
            self._delete_fixup(x)

    def _find_by_key(self, key):
        node = self._root
        while node != self._sentinel:
            if node.key == key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _find_maximum(self, node):
        while node.right != self._sentinel:
            node = node.right
        return node

    def _find_minimum(self, node):
        while node.left != self._sentinel:
            node = node.left
        return node

    def _find_predecessor(self, node):
        if node.left != self._sentinel:
            return self._find_maximum(node.left)
        parent = node.parent
        while parent != self._sentinel and node.is_left_child:
            node = parent
            parent = node.parent
        return parent

    def _find_successor(self, node):
        if node.right != self._sentinel:
            return self._find_minimum(node.right)
        parent = node.parent
        while parent != self._sentinel and node.is_right_child:
            node = parent
            parent = node.parent
        return parent

    def _insert_fixup(self, z):
        while z != self._root and z.parent.red:
            if z.parent.is_left_child:
                y = z.parent.parent.right
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z.is_right_child:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self._rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.red:
                    z.parent.red = False
                    y.red = False
                    z.parent.parent.red = True
                    z = z.parent.parent
                else:
                    if z.is_left_child:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.red = False
                    z.parent.parent.red = True
                    self._rotate_left(z.parent.parent)
        self._root.red = False

    def _insert_node(self, z):
        y = self._sentinel
        x = self._root
        while x != self._sentinel:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self._sentinel:
            self._root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        z.left = z.right = self._sentinel
        z.red = True
        self._insert_fixup(z)

    def _rotate_left(self, x):
        y = x.right

        x.right = y.left
        if y.left != self._sentinel:
            y.left.parent = x

        if y != self._sentinel:
            y.parent = x.parent

        if x.parent == self._sentinel:
            self._root = y
        elif x != self._sentinel:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y

        y.left = x
        if x != self._sentinel:
            x.parent = y

    def _rotate_right(self, x):
        y = x.left

        x.left = y.right
        if y.right != self._sentinel:
            y.right.parent = x

        if y != self._sentinel:
            y.parent = x.parent

        if x.parent == self._sentinel:
            self._root = y
        elif x != self._sentinel:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y

        y.right = x
        if x != self._sentinel:
            x.parent = y

    def _sort_nodes_inorder(self):
        def recurse(node):
            nodes = []
            if node.left != self._sentinel:
                nodes.extend(recurse(node.left))
            nodes.append(node)
            if node.right != self._sentinel:
                nodes.extend(recurse(node.right))
            return nodes
        if self._root != self._sentinel:
            return recurse(self._root)
        else:
            return []
