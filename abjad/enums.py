"""
Enumerations.
"""

import uqbar.enums


class Comparison(uqbar.enums.StrictEnumeration):
    """
    Enumeration of amount comparisons.
    """
    Less = -1
    Exact = 0
    More = 1

    def __format__(self, format_spec):
        return repr(self)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class HorizontalAlignment(uqbar.enums.StrictEnumeration):
    """
    Enumeration of horizontal alignments.
    """
    Left = -1
    Both = 0
    Right = 1

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class VerticalAlignment(uqbar.enums.StrictEnumeration):
    """
    Enumeration of vertical alignments.
    """
    Down = -1
    Center = 0
    Up = 1

    def __format__(self, format_spec):
        """
        Formats vertical alignment as ``storage`` or ``lilypond``.
        """
        if format_spec == 'lilypond':
            return {
                self.Down: '_',
                self.Up: '^',
                self.Center: '-',
            }[self]
        return repr(self)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @classmethod
    def from_expr(cls, expr):
        lilypond_symbols = {
            '^': cls.Up,
            '-': cls.Center,
            '_': cls.Down,
        }
        result = lilypond_symbols.get(expr)
        if result is not None:
            return result
        return super().from_expr(expr)


Both = HorizontalAlignment.Both
Center = VerticalAlignment.Center
Down = VerticalAlignment.Down
Exact = Comparison.Exact
Left = HorizontalAlignment.Left
Less = Comparison.Less
More = Comparison.More
Right = HorizontalAlignment.Right
Up = VerticalAlignment.Up


__all__ = [
    'Both',
    'Center',
    'Comparison',
    'Down',
    'Exact',
    'HorizontalAlignment',
    'Left',
    'Less',
    'More',
    'Right',
    'Up',
    'VerticalAlignment',
    ]
