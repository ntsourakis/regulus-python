#!/usr/bin/python

import sys
sys.path.append('./dante/python/')
sys.path.append('/app/poetry/python/')

import lite_call_runtime as call_main
#import sys
#sys.path.append('C:/Projects/django/callector/api/python/')
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# Use this to load table file from canonical place in zipfile (speech interface)
def init():
    TableFile = 'call_tables.data.gz'
    MatchingFile = 'robust_matching_tables.data.gz'
    return call_main.init_state(TableFile, MatchingFile)

# Use this to load table file from canonical place in zipfile (web-server interface)
def init_basic():
    #TODO
    TableFile = dir_path + '\call_tables.data.gz'
    MatchingFile = dir_path + '\\robust_matching_tables.data.gz'
    return call_main.init_state_basic(TableFile, MatchingFile)

# Top-level call for Alexa version: string to string
def string_and_state_to_action(String, State):
    return call_main.string_and_state_to_action_main(String, State)

# Top-level call for web-server version: json to json
def message_and_state_to_message(Message, State):
    return call_main.process_call_message(Message, State)

# Top-level call for doing robust matching (either version)
def robust_match(String, State, N):
    return call_main.robust_match_string(String, State, N)

# Convenient for testing on local machine (Alexa apps)
def init_local(Dir0):
    LocalCompiledDir = 'c:/cygwin64/home/speech/reguluslitecontent-svn/trunk/litecontent/alexa_content/compiled/'
    Dir = LocalCompiledDir + Dir0 + '/'
    TableFile = Dir + 'call_tables.data.gz'
    MatchingFile = Dir + 'robust_matching_tables.data.gz'
    return call_main.init_state(TableFile, MatchingFile)

#  Possible values:
#  'quel_animal'
#  'zahlenspiel'
#  'welches_tier'
#  'number_game'
#  'which_language'
#  'which_movie'
#  'jeu_de_chiffres'
#  'quelle_langue'

# Convenient for testing on local machine (web-server apps)

def init_dante():
    Dir = 'c:/cygwin64/home/speech/reguluslitecontent-svn/trunk/litecontent/alexa_content/compiled/dante/'
    TableFile = Dir + 'call_tables.data.gz'
    return call_main.init_state_basic(TableFile)

# import lite_call_runtime_top as call
# (State, Init, Bad) = call.init_local('quelle_langue')
# call.string_and_state_to_action('aide', State)
# call.robust_match('vassili', State, 2)

# State = call.init_dante()
# call.message_and_state_to_message(['get_available_lessons'], State)
# call.message_and_state_to_message(['set_lesson_by_name', 'Inferno I 1-30'], State)
# call.message_and_state_to_message(['help_file'], State)
# call.message_and_state_to_message(['spoken_help'], State)
# call.message_and_state_to_message(['match', 'mi ritrovai per una selva oscura'], State)
