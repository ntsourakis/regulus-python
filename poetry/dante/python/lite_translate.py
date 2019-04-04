#!/usr/bin/python

import dante.python.lite_grammar_match as lgm
import dante.python.lite_grammar_match_tables as lgm_tables

import pprint

pp = pprint.PrettyPrinter(indent=4, width=120)

# LOADING SPECIFIC TABLES 

babeldr_eng2_dir = 'C:/cygwin64/home/speech/reguluslitecontent-svn/trunk/LiteContent/tmp/babeldr_eng2/'
babeldr_eng2_parser_tables = babeldr_eng2_dir + 'babeldr_eng2_parser.data.gz'
babeldr_eng2_translation_tables = babeldr_eng2_dir + 'babeldr_eng2_translation.data.gz'
babeldr_eng2_tts_tables = babeldr_eng2_dir + 'babeldr_eng2_audio.data.gz'

babeldr_dir = 'C:/cygwin64/home/speech/BabelDr/LiteContent/tmp/babeldr_full/'
babeldr_parser_tables = babeldr_dir + 'babeldr_parser.data.gz'
babeldr_translation_tables = babeldr_dir + 'babeldr_translation.data.gz'
babeldr_audio_tables = babeldr_dir + 'babeldr_audio.data.gz'

# Load all tables for full BabelDr/French
def load_babeldr_french():
    lgm_tables.load_data(babeldr_parser_tables, 'babeldr')
    lgm_tables.load_translation_file_data(babeldr_translation_tables, 'babeldr')
    lgm_tables.load_tts_file_data(babeldr_audio_tables, 'babeldr')

# Load just parsing tables for 20170101 BabelDr/French
def load_babeldr_french_20170101():
    lgm_tables.load_data('c:/cygwin64/home/speech/medslt-code/trunk/medslt2/fre/generatedfiles/babeldr_tmp_python_tables.data.gz',
                     'babeldr')

# Load just parsing tables for toy version of BabelDr/French
def load_babeldr_small():
    lgm_tables.load_data('c:/cygwin64/home/speech/medslt-code/trunk/medslt2/fre/generatedfiles/babeldr_tmp_python_tables_small.data.gz',
                     'babeldr')

# Load all tables for BabelDr/English
def load_babeldr_english():
    lgm_tables.load_data(babeldr_eng2_parser_tables, 'babeldr_eng2')
    lgm_tables.load_translation_file_data(babeldr_eng2_translation_tables, 'babeldr_eng2')
    lgm_tables.load_tts_file_data(babeldr_eng2_tts_tables, 'babeldr_eng2')

# TOP-LEVEL CALLS

def print_match_translate_and_audio(InputString, NReturned, Namespace, Domain, TargetLanguage):
    global pp
    pp.pprint(match_translate_and_audio(InputString, NReturned, Namespace, Domain, TargetLanguage))

def match_translate_and_audio(InputString, NReturned, Namespace, Domain, TargetLanguage):
    return [ translate_and_audio(Match, Namespace, Domain, TargetLanguage) for Match in
             lgm.match_string(InputString, NReturned, Namespace, Domain) ]

def translate_and_audio(Match, Namespace, Domain, TargetLanguage):
    if 'canonical' in Match:
        Translation = translation_for_canonical(Match['canonical'], Namespace, Domain, TargetLanguage)
        AudioFile = tts_file_for_translation(Translation, Namespace, Domain, TargetLanguage)
        Match['translation'] = Translation
        Match['audio_file'] = AudioFile
    return Match

# Get a translation from the translation table for a given canonical
def translation_for_canonical(Canonical, Namespace, Domain, TargetLanguage):
    Key0 = tuple([Namespace])
    Key = tuple([Canonical, Namespace, Domain])
    if ( Key0 in lgm_tables.translations and Key in lgm_tables.translations[Key0] and TargetLanguage in lgm_tables.translations[Key0][Key][0] ):
        return lgm_tables.translations[Key0][Key][0][TargetLanguage]
    else:
        return "no_translation"

# Get the TTS file for a given translation
def tts_file_for_translation(TargetString, Namespace, Domain, TargetLanguage):
    Key0 = tuple([Namespace])
    Key = tuple([TargetString, Namespace, Domain, TargetLanguage])
    if ( Key0 in lgm_tables.tts_file and Key in lgm_tables.tts_file[Key0] ):
        return lgm_tables.tts_file[Key0][Key][0]
    else:
        return "no_tts_file"

# Get all the TTS files (useful if you're going to copy them from the directory where they're created)
def all_loaded_tts_files(Namespace, Domain):
    Key0 = tuple([Namespace])
    if lgm_tables.tts_file == 'null':
        return 'no TTS files loaded'
    elif not Key0 in lgm_tables.tts_file:
        return 'no TTS files loaded for this namespace and domain'
    else:
        return [ lgm_tables.tts_file[Key0][Key][0] for Key in lgm_tables.tts_file[Key0] ]
 
