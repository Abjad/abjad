# -*- encoding: utf-8 -*-
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


class ResidueClass(BaseResidueClass):
    r'''Residue class (or congruence class).

    Residue classes form the basis of Xenakis sieves. They can be used to
    make any complex periodic integer or boolean sequence as a
    combination of simple periodic sequences.

    ..  container:: example

        **Example.** From the opening of Xenakis's *Psappha* for solo 
        percussion:

        ::

            >>> RC = sievetools.ResidueClass

        ::

            >>> s1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
            >>> s2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
            >>> s3 = RC(8, 3)
            >>> s4 = RC(8, 4)
            >>> s5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
            >>> s6 = (RC(8, 1) & RC(5, 2))
            >>> s7 = (RC(8, 6) & RC(5, 1))

        ::

            >>> y = s1 | s2 | s3 | s4 | s5 | s6 | s7

        ::

            >>> y.get_congruent_bases(40)
                [0, 1, 3, 4, 6, 8, 10, 11, 12, 13, 14, 16, 17, 19, 20, 22, 
                23, 25, 27, 28, 29, 31, 33, 35, 36, 37, 38, 40]

        ::

            >>> y.get_boolean_train(40)
                [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 
                1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0]

    Return residue class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_modulo', 
        '_residue',
        )

    ### INITIALIZER ##

    def __init__(self, *args):
        if len(args) == 1:
            self._init_by_rc_instance(*args)
        elif len(args) == 2:
            self._init_by_modulo_and_residue(*args)
        else:
            raise ValueError('unknown init arguments.')

    ### SPECIAL METHODS ###

    def __eq__(self, exp):
        if isinstance(exp, ResidueClass):
            return (self.modulo == exp.modulo) and \
                (self.residue == exp.residue)
        else:
            return False

    def __ge__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return expr.residue <= self.residue
        return expr.modulo <= self.modulo

    def __gt__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return expr.residue < self.residue
        return expr.modulo < self.modulo

    def __le__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return self.residue <= expr.residue
        return self.modulo <= expr.modulo

    def __lt__(self, expr):
        if not isinstance(expr, ResidueClass):
            raise TypeError('must be residue class.')
        if self.modulo == expr.modulo:
            return self.residue < expr.residue
        return self.modulo < expr.modulo

    def __ne__(self, expr):
        return not self == expr

    def __repr__(self):
        return '%s(%i, %i)' % (self._class_name, self.modulo, self.residue)

    ### PRIVATE METHODS ###

    def _init_by_modulo_and_residue(self, modulo, residue):
        if not 0 < modulo:
            raise ValueError('modulo must be positive.')
        if not 0 <= residue < modulo:
            raise ValueError('abs(residue) must be < modulo')
        self._modulo = modulo
        self._residue = residue

    def _init_by_rc_instance(self, rc):
        if not isinstance(rc, ResidueClass):
            raise TypeError('must be rc instance.')
        self._modulo = rc.modulo
        self._residue = rc.residue

    ### PUBLIC PROPERTIES ###

    @property
    def modulo(self):
        r'''Period of residue class.
        '''
        return self._modulo

    @property
    def residue(self):
        r'''Residue of residue class.
        '''
        return self._residue

    ### PUBLIC METHODS ###

    def get_boolean_train(self, *min_max):
        r'''Returns a boolean train with 0s mapped to the integers
        that are not congruent bases of the residue class and 1s mapped
        to those that are.

        The method takes one or two integer arguments. If only one is given,
        it is taken as the max range and the min is assumed to be 0.

        ..  container:: example

            **Example:**

            ::

                >>> r = RC(3, 0)
                >>> r.get_boolean_train(6)
                [1, 0, 0, 1, 0, 0]

            ::

                >>> r.get_congruent_bases(-6, 6)
                [-6, -3, 0, 3, 6]

        Return list.
        '''
        minimum, maximum = self._process_min_max_attribute(*min_max)
        result = []
        for i in range(minimum, maximum):
            if i % self.modulo == self.residue:
                result.append(1)
            else:
                result.append(0)
        return result

    def get_congruent_bases(self, *min_max):
        r'''Returns all the congruent bases of this residue class within the 
        given range.

        The method takes one or two integer arguments. If only one it given, it 
        is taken as the max range and the min is assumed to be 0.

        ..  container:: example

            **Example:**

            ::

                >>> r = RC(3, 0)
                >>> r.get_congruent_bases(6)
                [0, 3, 6]

            ::

                >>> r.get_congruent_bases(-6, 6)
                [-6, -3, 0, 3, 6]

        Return list.
        '''
        minimum, maximum = self._process_min_max_attribute(*min_max)
        result = []
        for i in range(minimum, maximum + 1):
            if i % self.modulo == self.residue:
                result.append(i)
        return result


if __name__ == '__main__':
    print 'Psappha B2[0:40]'
    RC = ResidueClass
    s1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
    s2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
    s3 = RC(8, 3) #&  RC(1, 0)
    s4 = RC(8, 4) #&  RC(1, 0)
    s5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
    s6 = (RC(8, 1) & RC(5, 2))
    s7 = (RC(8, 6) & RC(5, 1))

    y = s1 | s2 | s3 | s4 | s5 | s6 | s7
    print y
    print 'congruent bases:\n', y.get_congruent_bases(40)
    print 'boolen train:\n', y.get_boolean_train(40)
