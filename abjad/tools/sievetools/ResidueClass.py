# -*- encoding: utf-8 -*-
import functools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


@functools.total_ordering
class ResidueClass(BaseResidueClass):
    r'''Residue class (or congruence class).

    Residue classes form the basis of Xenakis sieves. They can be used to
    make any complex periodic integer or boolean sequence as a
    combination of simple periodic sequences.

    ..  container:: example

        From the opening of Xenakis's *Psappha* for solo percussion:

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

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_modulo',
        '_residue',
        )

    ### INITIALIZER ##

    def __init__(self, *args):
        if len(args) == 1:
            self._initialize_by_rc_instance(*args)
        elif len(args) == 2:
            self._initialize_by_modulo_and_residue(*args)
        elif len(args) == 0:
            self._initialize_by_modulo_and_residue(1, 0)
        else:
            message = 'can not intialize residue class: {!r}.'
            message = message.format(args)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a residue class with module and residue equal
        to those of this residue class. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, ResidueClass):
            if self.modulo == expr.modulo:
                if self.residue == expr.residue:
                    return True
        return False

    def __hash__(self):
        r'''Hashes residue class.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(ResidueClass, self).__hash__()

    def __lt__(self, expr):
        r'''Is true when `expr` is a residue class with module greater than that
        of this residue class. Also true when `expr` is a residue class with
        modulo equal to that of this residue class and with residue greater
        than that of this residue class. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, ResidueClass):
            if self.modulo == expr.modulo:
                return self.residue < expr.residue
            return self.modulo < expr.modulo

    def __ne__(self, expr):
        r'''Is true when `expr` is not equal to this residue class. Otherwise
        false.

        Return boolean.
        '''
        return not self == expr

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                self.modulo,
                self.residue,
                ),
            )

    ### PRIVATE METHODS ###

    def _initialize_by_modulo_and_residue(self, modulo, residue):
        if not 0 < modulo:
            message = 'modulo must be positive: {!r}.'
            message = message.format(modulo)
            raise ValueError(message)
        if not 0 <= residue < modulo:
            message = 'abs(residue) must be < modulo.'
            raise ValueError(message)
        self._modulo = modulo
        self._residue = residue

    def _initialize_by_rc_instance(self, rc):
        if not isinstance(rc, ResidueClass):
            message = 'must be residue class: {!r}.'
            message = message.format(rc)
            raise TypeError(message)
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

            ::

                >>> r = RC(3, 0)
                >>> r.get_boolean_train(6)
                [1, 0, 0, 1, 0, 0]

            ::

                >>> r.get_congruent_bases(-6, 6)
                [-6, -3, 0, 3, 6]

        Returns list.
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

            ::

                >>> r = RC(3, 0)
                >>> r.get_congruent_bases(6)
                [0, 3, 6]

            ::

                >>> r.get_congruent_bases(-6, 6)
                [-6, -3, 0, 3, 6]

        Returns list.
        '''
        minimum, maximum = self._process_min_max_attribute(*min_max)
        result = []
        for i in range(minimum, maximum + 1):
            if i % self.modulo == self.residue:
                result.append(i)
        return result


if __name__ == '__main__':
    print('Psappha B2[0:40]')
    RC = ResidueClass
    s1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
    s2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
    s3 = RC(8, 3) #&  RC(1, 0)
    s4 = RC(8, 4) #&  RC(1, 0)
    s5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
    s6 = (RC(8, 1) & RC(5, 2))
    s7 = (RC(8, 6) & RC(5, 1))

    y = s1 | s2 | s3 | s4 | s5 | s6 | s7
    print(y)
    print('congruent bases:\n', y.get_congruent_bases(40))
    print('boolen train:\n', y.get_boolean_train(40))