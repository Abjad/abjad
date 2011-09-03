from abjad.cfg._config_file_dict import _config_file_dict
from abjad.cfg._config_file_to_dict import _config_file_to_dict
from abjad.cfg._update_config_file import _update_config_file
from abjad.cfg._write_config_file import _write_config_file
from abjad.cfg.cfg import ABJADCONFIG


def _verify_config_file( ):
    try:
        f = open(ABJADCONFIG, 'r')
        f.close( )
        user_dict = _config_file_to_dict( )

        # TODO: This block overwrites user-specific config file additions like 'foo = 99' #
        #         Fix and allow user-specific config file additions?                                #
        #         Or remove the message about old keys being maintained?                          #

        default_keyset = set(_config_file_dict.keys( ))
        user_keyset = set(user_dict.keys( ))
        if default_keyset.intersection(user_keyset) != default_keyset:
            print ''
            print '   The config file "%s" in your home directory is out of date.' % ABJADCONFIG
            print '   Abjad will now overwrite the old file with a new one.'
            print '   Any custom keys from your old configuration will be maintained.'
            print ''
            raw_input('   Press any key to continue: ')
            _update_config_file(_config_file_dict, user_dict)

    except IOError:
        print ''
        print '   Abjad will now create the file "%s" in your home directory.' % ABJADCONFIG
        print '   Edit this file to change the way Abjad starts up and runs.'
        print ''
        raw_input('   Press any key to continue: ')
        print ''
        _write_config_file(ABJADCONFIG, _config_file_dict)
