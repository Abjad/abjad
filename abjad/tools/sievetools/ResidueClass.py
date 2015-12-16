# -*- coding: utf-8 -*-
import functools
from abjad.tools.sievetools.BaseResidueClass import BaseResidueClass


@functools.total_ordering
class ResidueClass(BaseResidueClass):
    r'''Residue class.

    A residue class is a simple periodic sequence.

    Residue classes can be combined with logical operators.

    Residue classes form the basis of Xenakis sieves.

    ..  container:: example

        From the opening of Xenakis's *Psappha* for solo percussion:

        ::

            >>> RC = sievetools.ResidueClass

        ::

            >>> sieve_1 = (RC(8, 0) | RC(8, 1) | RC(8, 7)) & (RC(5, 1) | RC(5, 3))
            >>> sieve_2 = (RC(8, 0) | RC(8, 1) | RC(8, 2)) & RC(5, 0)
            >>> sieve_3 = RC(8, 3)
            >>> sieve_4 = RC(8, 4)
            >>> sieve_5 = (RC(8, 5) | RC(8, 6)) & (RC(5, 2) | RC(5, 3) | RC(5, 4))
            >>> sieve_6 = (RC(8, 1) & RC(5, 2))
            >>> sieve_7 = (RC(8, 6) & RC(5, 1))

        ::

            >>> sieve = sieve_1 | sieve_2 | sieve_3 | sieve_4 | sieve_5 | sieve_6 | sieve_7

        ::

            >>> sieve.get_congruent_bases(40)
                [0, 1, 3, 4, 6, 8, 10, 11, 12, 13, 14, 16, 17, 19, 20, 22,
                23, 25, 27, 28, 29, 31, 33, 35, 36, 37, 38, 40]

        ::

            >>> sieve.get_boolean_train(40)
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
        r'''Is true when `expr` is a residue class with module and residue
        equal to those of this residue class. Otherwise false.

        Returns true or false.
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
        r'''Is true when `expr` is a residue class with module greater than 
        that of this residue class. Also true when `expr` is a residue class
        with modulo equal to that of this residue class and with residue 
        greater than that of this residue class. Otherwise false.

        Returns true or false.
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

    # TODO: change name to 'period'
    @property
    def modulo(self):
        r'''Gets modulo of residue class.

        Gets period of residue class.
        '''
        return self._modulo

    @property
    def residue(self):
        r'''Gets residue of residue class.
        '''
        return self._residue

    ### PUBLIC METHODS ###

    def get_boolean_train(self, *min_max):
        r'''Gets boolean train.

        ..  container:: example

            **Example 1.** Gets first eight values of boolean train:

                ::

                    >>> residue_class = RC(2, 0)
                    >>> residue_class.get_boolean_train(8)
                    [1, 0, 1, 0, 1, 0, 1, 0]

        ..  container:: example

            **Example 2.** Gets first eight values of boolean train:

                ::

                    >>> residue_class = RC(3, 0)
                    >>> residue_class.get_boolean_train(8)
                    [1, 0, 0, 1, 0, 0, 1, 0]

        Boolean train is defined equal to a list of ones and zeros: ones map to
        integers included in the residue class while zeroes map to integers not
        included in the residue class.

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
        r'''Gets congruent bases.
        
        ..  container:: example

            **Example 1.** Gets congruent bases:

                ::

                    >>> residue_class = RC(2, 0)
                    >>> residue_class.get_congruent_bases(8)
                    [0, 2, 4, 6, 8]

        ..  container:: example

            **Example 2.** Gets congruent bases:

                ::

                    >>> residue_class = RC(3, 0)
                    >>> residue_class.get_congruent_bases(8)
                    [0, 3, 6]

        Returns list.
        '''
        minimum, maximum = self._process_min_max_attribute(*min_max)
        result = []
        for i in range(minimum, maximum + 1):
            if i % self.modulo == self.residue:
                result.append(i)
        return result