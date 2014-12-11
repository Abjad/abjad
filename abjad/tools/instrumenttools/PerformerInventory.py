# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class PerformerInventory(TypedList):
    r'''Abjad model of an ordered list of performers.

    Performer inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        return systemtools.AttributeManifest()

    @property
    def _item_creator_class(self):
        item_creator_class = self._make_item_creator_class()
        return item_creator_class

    @property
    def _item_creator_class_kwargs(self):
        return {'is_ranged': True}

    ### PRIVATE METHODS ###

    @staticmethod
    def _initialize_performer(performer, session):
        from abjad.tools import instrumenttools
        menu = PerformerInventory._make_performer_configuration_menu(
            performer,
            session,
            )
        while True:
            result = menu._run()
            if menu._session.is_backtracking:
                return
            elif not result:
                continue
            if result in ('skip', ['skip']):
                break
            elif result in ('more', ['more']):
                inventory = instrumenttools.InstrumentInventory()
                class_ = inventory._make_item_creator_class()
                item_creator = class_(
                    session=session,
                    is_ranged=True,
                    )
                instruments = item_creator._run()
                if item_creator._session.is_backtracking:
                    break
                if instruments is not None:
                    for instrument in instruments:
                        performer.instruments.append(instrument)
                break
            elif isinstance(result, list):
                name = '_default_instrument_name_to_instrument_class'
                method = getattr(instrumenttools.Instrument, name)
                for instrument_name in result:
                    instrument_class = method(instrument_name)
                    instrument = instrument_class()
                    performer.instruments.append(instrument)
                break
            else:
                raise Exception("how'd we get here?")

    @staticmethod
    def _make_performer_configuration_menu(performer, session):
        from abjad.tools import instrumenttools
        menu = session._io_manager._make_menu(name='performer configuration')
        commands = []
        likely_instruments = \
            performer.likely_instruments_based_on_performer_name
        likely_instrument_names = [
            x().instrument_name for x in likely_instruments]
        likely_instrument_names.sort()
        most_likely_instrument = \
            performer.most_likely_instrument_based_on_performer_name
        default_index = None
        numbered_menu_entries = []
        if most_likely_instrument is not None:
            most_likely_instrument_name = \
                most_likely_instrument().instrument_name
            assert most_likely_instrument_name in likely_instrument_names
            most_likely_index = likely_instrument_names.index(
                most_likely_instrument_name)
            string = '{} (default)'.format(most_likely_instrument_name)
            likely_instrument_names[most_likely_index] = string
            most_likely_number = most_likely_index + 1
            default_index = most_likely_index
        if likely_instruments:
            numbered_menu_entries = likely_instrument_names
            commands.append(('instruments - more', 'more'))
        else:
            instrument_names = \
                instrumenttools.Instrument._list_instrument_names()
            numbered_menu_entries = instrument_names
        numbered_list_section = menu.make_numbered_list_section(
            default_index=default_index,
            group_by_annotation=False,
            menu_entries=numbered_menu_entries,
            name='select instruments',
            title='select instruments',
            )
        commands.append(('instruments - skip', 'skip'))
        menu.make_command_section(
            commands=commands,
            name='instrument commands',
            )
        return menu

    ### ITEM CREATOR ###

    @staticmethod
    def _make_item_creator_class():
        from ide.idetools.Controller import Controller
        class ItemCreator(Controller):
            ### CLASS VARIABLES ###
            __slots__ = ('_is_ranged', '_target')
            ### INITIALIZER ###
            def __init__(self, is_ranged=False, session=None, target=None):
                Controller.__init__(self, session=session)
                self._is_ranged = is_ranged
                self._target = target
            ### PRIVATE METHODS ###
            def _run(self):
                from abjad.tools import instrumenttools
                from ide import idetools
                try_again = False
                performers = []
                controller = idetools.ControllerContext(controller=self)
                selector = idetools.Selector(session=self._session)
                selector = selector.make_score_tools_performer_name_selector(
                    is_ranged=self._is_ranged,
                    )
                with controller:
                    while True:
                        result = selector._run()
                        if self._session.is_backtracking:
                            break
                        if isinstance(result, list):
                            performer_names = result
                        else:
                            performer_names = [result]
                        performers = []
                        Performer = instrumenttools.Performer
                        for performer_name in performer_names:
                            performer = Performer(performer_name)
                            PerformerInventory._initialize_performer(
                                performer,
                                self._session,
                                )
                            was_backtracking_locally = \
                                self._session.is_backtracking_locally
                            if self._session.is_backtracking:
                                if was_backtracking_locally:
                                    try_again = True
                                else:
                                    try_again = False
                                    performers = []
                                break
                            performers.append(performer)
                        if not try_again:
                            break
                        else:
                            try_again = False
                    if self._is_ranged and performers:
                        final_result = performers[:]
                    elif self._is_ranged and not performers:
                        final_result = []
                    elif not self._is_ranged and performers:
                        final_result = performers[0]
                    elif not self._is_ranged and not performers:
                        final_result = None
                    else:
                        raise ValueError
                    self._target = final_result
                    return self.target
            @property
            def target(self):
                return self._target
        return ItemCreator

    ### PUBLIC METHODS ###

    def get_instrument(self, instrument_name):
        r'''Gets first instrument in performer inventory with
        `instrument_name`.

        ..  container:: example

            ::
            
                >>> flutist = instrumenttools.Performer(name='flutist')
                >>> flutist.instruments.append(instrumenttools.Flute())
                >>> flutist.instruments.append(instrumenttools.Piccolo())
                >>> inventory = instrumenttools.PerformerInventory(
                ...     [flutist],
                ...     )
                >>> inventory.get_instrument('piccolo')
                Piccolo()

        Returns instrument or none.
        '''
        for performer in self:
            instrument = performer.get_instrument(instrument_name)
            if instrument is not None:
                return instrument