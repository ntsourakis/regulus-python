
import gzip, pickle

##all_data = {
##"rules_for_word":rules_for_word,
##"phrase_rule_for_matching":phrase_rule_for_matching,
##"phrase_rules_for_rule":phrase_rules_for_rule,
##"rule_for_matching":rule_for_matching,
##"minimum_score_for_rule":minimum_score_for_rule,
##"minimum_length_string_for_rule":minimum_length_string_for_rule,
##"canonical_sentence":canonical_sentence
##}

rules_for_word = {}
phrase_rule_for_matching = {}
phrase_rules_for_rule = {}
rule_for_matching = {}
minimum_score_for_rule = {}
minimum_length_string_for_rule = {}
canonical_sentence = {}
translations = {}
tts_file = {}

def check_tables_are_loaded():
    global rules_for_word
    global rule_for_matching
    if rules_for_word == {}:
        print('*** Warning: robust matching table rules_for_word has not been initialised')
    if rule_for_matching == {}:
        print('*** Warning: robust matching table rule_for_matching has not been initialised')

def load_data(tables_file, Namespace):
    global rules_for_word
    global phrase_rule_for_matching
    global phrase_rules_for_rule
    global rule_for_matching
    global minimum_score_for_rule
    global minimum_length_string_for_rule
    global canonical_sentence
    
    f = gzip.open(tables_file, 'rb')
    all_data = pickle.load(f)
    f.close()
    print('Loaded grammar matching table data from {}'.format(tables_file))

    Key = tuple([Namespace])
    
    rules_for_word[Key] = component(all_data, 'rules_for_word')
    phrase_rule_for_matching[Key] = component(all_data, 'phrase_rule_for_matching')
    phrase_rules_for_rule[Key] = component(all_data, 'phrase_rules_for_rule')
    rule_for_matching[Key] = component(all_data, 'rule_for_matching')
    minimum_score_for_rule[Key] = component(all_data, 'minimum_score_for_rule')
    minimum_length_string_for_rule[Key] = component(all_data, 'minimum_length_string_for_rule')
    canonical_sentence[Key] = component(all_data, 'canonical_sentence')

def load_translation_file_data(tables_file, Namespace):
    global translations
    
    f = gzip.open(tables_file, 'rb')
    all_data = pickle.load(f)
    f.close()
    print('Loaded translation file table data from {}'.format(tables_file))

    Key = tuple([Namespace])
    
    translations[Key] = component(all_data, 'translations')

def load_tts_file_data(tables_file, Namespace):
    global tts_file
    
    f = gzip.open(tables_file, 'rb')
    all_data = pickle.load(f)
    f.close()
    print('Loaded TTS file table data from {}'.format(tables_file))

    Key = tuple([Namespace])
    
    tts_file[Key] = component(all_data, 'tts_file')

def component(all_data, component_name):
    if all_data == 'null':
        print('*** Error: no data loaded')
    elif component_name in all_data:
        return all_data[component_name]
    else:
        print('*** Warning: no table called {}'.format(component_name))

