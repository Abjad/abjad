from abjad.cfg.cfg import ABJADCONFIG


def verify_abjad_user_config_file():
    from abjad.tools import configurationtools

    default_dict = configurationtools.make_abjad_default_config_file_into_dict()
    try:
        user_dict = configurationtools.make_abjad_user_config_file_into_dict()

        # TODO: This block overwrites user-specific config file additions like 'foo = 99'
        #         Fix and allow user-specific config file additions?
        #         Or remove the message about old keys being maintained?
        default_keyset = set(configurationtools.make_abjad_default_config_file_into_dict().keys())
        user_keyset = set(user_dict.keys())
        if default_keyset.intersection(user_keyset) != default_keyset:
            print ''
            print '   The config file "%s" in your home directory is out of date.' % ABJADCONFIG
            print '   Abjad will now overwrite the old file with a new one.'
            print '   Any custom keys from your old configuration will be maintained.'
            print ''
            raw_input('   Press any key to continue: ')
            configurationtools.update_abjad_user_config_file(default_dict, user_dict)

    except IOError:
        print ''
        print '   Abjad will now create the file "%s" in your home directory.' % ABJADCONFIG
        print '   Edit this file to change the way Abjad starts up and runs.'
        print ''
        raw_input('   Press any key to continue: ')
        print ''
        configurationtools.write_abjad_user_config_file(ABJADCONFIG, default_dict)
