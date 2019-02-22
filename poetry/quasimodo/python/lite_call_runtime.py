#!/usr/bin/python

import quasimodo.python.lite_call_output_manager as output_manager
import quasimodo.python.lite_call_tables as tables
import quasimodo.python.lite_call_scores as scores
import quasimodo.python.lite_call_logging as log

import quasimodo.python.lite_grammar_match as lgm
import quasimodo.python.lite_grammar_match_tables as lgm_tables
import quasimodo.python.lite_grammar_match_regularise as lgm_regularise

import random

# TOP-LEVEL CALLS

# Call this to init and get an initial State, an initial Action and a "don't understand" message
def init_state(TableFile, RobustMatchFile):
    random.seed()
    log.print_log_message(['load_tables', TableFile])
    NamespaceEtc = tables.load_data(TableFile)
    ( Namespace, Domain, L2, L1 ) = ( NamespaceEtc['namespace'], NamespaceEtc['domain'], NamespaceEtc['l2'], NamespaceEtc['l1'] )
    log.print_log_message(['load_tables_succeeded', { 'namespace':Namespace, 'domain':Domain, 'l2':L2, 'l1':L1 }] )
    log.print_log_message(['load_robust_matching_tables', RobustMatchFile])
    lgm_tables.load_data(RobustMatchFile, Namespace)
    log.print_log_message(['load_robust_matching_tables_succeeded', RobustMatchFile, Namespace])
    #add_regularised_keys_to_sent_atom_namespace_lf_l1_text(Namespace, Domain)
    State = initial_state()
    process_call_message(['set_namespace_domain_and_language', Namespace, Domain, L1], State)
    import_course_info_into_state(State)
    #State['l2'] = L2
    FirstLesson = get_available_lessons(State)['lessons'][0]
    AbstractAction = process_call_message(['set_lesson', FirstLesson], State)
    InitialAction = output_manager.abstract_call_action_to_action(AbstractAction, L1, L2)
    if 'text_to_repeat' in InitialAction:
        State['text_to_repeat'] = InitialAction['text_to_repeat']
    output_manager.prepend_invocation_name_to_action_text(InitialAction, State)
    DontUnderstandAction = output_manager.dont_understand_action(L1, L2, State)
    log.print_log_message(['initialised', { 'state':State,
                                            'initial_action':InitialAction,
                                            'dont_understand_action':DontUnderstandAction } ])
    return ( State, InitialAction, DontUnderstandAction )

# Call this to init and get an initial State
def init_state_basic(TableFile, RobustMatchFile):
    random.seed()
    log.print_log_message(['load_tables', TableFile])
    NamespaceEtc = tables.load_data(TableFile)
    ( Namespace, Domain, L2, L1 ) = ( NamespaceEtc['namespace'], NamespaceEtc['domain'], NamespaceEtc['l2'], NamespaceEtc['l1'] )
    log.print_log_message(['load_tables_succeeded', { 'namespace':Namespace, 'domain':Domain, 'l2':L2, 'l1':L1}])
    log.print_log_message(['load_robust_matching_tables', RobustMatchFile])
    lgm_tables.load_data(RobustMatchFile, Namespace)
    log.print_log_message(['load_robust_matching_tables_succeeded', RobustMatchFile, Namespace])
    #add_regularised_keys_to_sent_atom_namespace_lf_l1_text(Namespace, Domain)
    State = initial_state()
    process_call_message(['set_namespace_domain_and_language', Namespace, Domain, L1], State)
    import_course_info_into_state(State)
    #State['l2'] = L2
    return State

# Call this to process a string and get a response, updating the State
# Language is the output language
def string_and_state_to_action_main(String0, State):
    log.print_log_message(['process_string', String0])
    check_tables_are_loaded()
    String = robust_process_string_for_call(String0, State)
    L1 = State['language']
    L2 = State['l2']
    MessageInterpretation = string_as_call_message(String, State)
    if MessageInterpretation:
        log.print_log_message(['interpretation', MessageInterpretation])
        AbstractAction1 = process_call_message(MessageInterpretation, State)
    else:
        log.print_log_message(['interpretation', ['match', String]])
        AbstractAction1 = process_call_message(['match', String], State)
    Action1 = output_manager.abstract_call_action_to_action(AbstractAction1, L1, L2)
    Action = do_auto_next_if_necessary(Action1, State, L1, L2)
    if 'text_to_repeat' in Action:
        State['text_to_repeat'] = Action['text_to_repeat']
    log.print_log_message(['response', Action])
    return Action

def do_auto_next_if_necessary(Action1, State, L1, L2):
    if 'auto_next' in Action1 and Action1['auto_next'] == 'auto_next':
        AbstractAction2 = process_call_message(['auto_next'], State)
        Action2 = output_manager.abstract_call_action_to_action(AbstractAction2, L1, L2)
        Action2['text'] = Action1['text'] + Action2['text']
        return do_auto_next_if_necessary(Action2, State, L1, L2)
    elif 'auto_next' in Action1 and Action1['auto_next'] == 'next_lesson':
        AbstractAction2 = process_call_message(['next_lesson'], State)
        Action2 = output_manager.abstract_call_action_to_action(AbstractAction2, L1, L2)
        Action2['text'] = Action1['text'] + Action2['text']
        return do_auto_next_if_necessary(Action2, State, L1, L2)
    else:
        return Action1

# ----------------------------------------

## process_call_message(Message, State)
##
## Possible messages:
##
## ['get_available_namespaces_domains_and_l1s']
##
## ['set_namespace_domain_and_language', Namespace, Domain, Language]
##
## ['get_available_lessons']
##
## ['set_lesson', Lesson]
##
## ['set_lesson_by_name', Lesson]
##
## ['next_lesson']
##
## ['next']
##
## ['back']
##
## ['help']
##
## ['spoken_help']
##
## ['help_file']
##
## ['repeat']
##
## ['wait']
##
## ['match', String]
##
## ['exit']

def well_formed_message(Message):
    if not isinstance(Message, (list, tuple)):
        return False
    elif ( Message[0] == 'get_available_namespaces_domains_and_l1s' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'set_namespace_domain_and_language' and len(Message) == 4 ):
        return True
    elif ( Message[0] == 'get_available_lessons' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'set_lesson' and len(Message) == 2 ):
        return True
    elif ( Message[0] == 'set_lesson_by_name' and len(Message) == 2 ):
        return True
    elif ( Message[0] == 'next_lesson' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'next' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'auto_next' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'back' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'help' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'spoken_help' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'help_file' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'repeat' and len(Message) == 1 ):
        return True
    elif ( Message[0] == 'wait' and len(Message) == 1 ):
        return True
    elif Message[0] == 'match' and len(Message) == 2:
        return True
    elif ( Message[0] == 'exit' and len(Message) == 1 ):
        return True
    else:
        return False

def process_call_message(Message, State):
    if not well_formed_message(Message):
        return 'ill_formed_message'
    elif Message[0] == 'get_available_namespaces_domains_and_l1s':
        return get_available_namespaces_domains_and_l1s()
    elif Message[0] == 'set_namespace_domain_and_language':
        return set_namespace_domain_and_language(State, Message[1], Message[2], Message[3])
    elif Message[0] == 'get_available_lessons':
        return get_available_lesson_names(State)
    elif Message[0] == 'set_lesson':
        return set_lesson(State, Message[1])
    elif Message[0] == 'set_lesson_by_name':
        return set_lesson_by_name(State, Message[1])
    elif Message[0] == 'next_lesson':
        return set_next_lesson(State)
    elif Message[0] == 'next':
        return set_next_prompt(State)
    elif Message[0] == 'auto_next':
        return set_next_prompt_auto(State)
    elif Message[0] == 'back':
        return go_back(State)
    elif Message[0] == 'help':
        return get_help(State)
    elif Message[0] == 'spoken_help':
        return get_spoken_help(State)
    elif Message[0] == 'help_file':
        return get_help_file(State)
    elif Message[0] == 'repeat':
        return get_last_system_utterance(State)
    elif Message[0] == 'wait':
        return wait(State)
    elif Message[0] == 'match':
        return match(Message[1], State)
    elif Message[0] == 'exit':
        return exit_game(State)
    else:
        return { 'error':'internal_error' }

def initial_state():
    return {}

# Tries to turn String into a well-formed message in the context of State. Returns False if it can't do that.

def string_as_call_message(String, State):
    Key0 = tuple([State['namespace']])
    Key = tuple([ String, State['namespace'], State['domain'], 'command' ])
    if ( Key0 in tables.sent_atom_namespace_lf_l1_text and Key in tables.sent_atom_namespace_lf_l1_text[Key0] ):
        Possibilities = tables.sent_atom_namespace_lf_l1_text[Key0][Key][0]
    else:
        return False
    Command = Possibilities[0][1].split()
    if well_formed_message(Command):
        return Command
    else:
        return False

# ----------------------------------------

def set_namespace_domain_and_language(State, Namespace, Domain, Language):
    if valid_namespace_domain_and_language(Namespace, Domain, Language):
        State['namespace'] = Namespace
        State['domain'] = Domain
        State['language'] = Language
        return 'ok'
    else:
        return 'error'

def set_next_lesson(State):
    return set_lesson(State, get_next_lesson(State))

def set_lesson_by_name(State, LessonName):
    return set_lesson(State, lesson_for_name(LessonName, State))

def set_lesson(State, Lesson):
    if valid_lesson_in_state(State, Lesson):
        State['lesson'] = Lesson
        State['forwardList'] = forward_list_for_all_prompts(State)
        State['allHelpTexts'] = forward_list_to_all_examples_list(State['forwardList'])
        NextPromptAction = set_next_prompt(State)
        # We throw away the back-list, since we're only allowing people to go back to the beginning of the lesson
        State['backList'] = []
        return merge_dicts( NextPromptAction,
                            { 'response_to':'set_lesson',
                              'lesson':name_for_lesson(Lesson, State),
                              'number_of_lessons':number_of_lessons_in_state(State) } )
    else:
        return { 'response_to':'set_lesson',
                 'error':'unknown_lesson',
                 'lesson':Lesson}

def forward_list_to_all_examples_list(ForwardList):
    return list(set([ X['example'] for X in ForwardList ]))

def set_next_prompt_auto(State):
    Action = set_next_prompt(State)
    Action['response_to'] = 'auto_next'
    return Action

def set_next_prompt(State):
    if 'forwardList' in State and len(State['forwardList']) > 0 :
        return set_next_prompt_using_forward_list(State)
    else:
        return { 'response_to':'next', 'error':'no_more_prompts_in_lesson',
                 'score':State['score'], 'max_possible_score':State['max_possible_score'] }

# If we have a forwardList defined, we're undoing a 'back' action.
# 
def set_next_prompt_using_forward_list(State):
    ForwardList = State['forwardList']
    NextItemInForwardList = ForwardList[0]
    if forward_or_back_list_item_from_state(State):
        push_item_onto_back_list(State, forward_or_back_list_item_from_state(State))
    update_state_from_forward_or_back_list_item(State, NextItemInForwardList)
    State['forwardList'] = ForwardList[1:]
    Prompt = { 'type':'prompt', 'response_to':'next', 'text':State['prompt'] }
    return Prompt

# We no longer use this, since we compute all the prompts when we set the lesson
# and put them on the forwardList

##def set_next_prompt_normal(State):
##    AllPrompts = prompts_for_state(State)
##    Groups = list(AllPrompts.keys())
##    RandomGroup = random_member(Groups)
##    PromptRecordsForGroup = AllPrompts[RandomGroup]
##    RandomPromptRecord = random_member(PromptRecordsForGroup)
##    PromptText = RandomPromptRecord[0][State['language']]
##    Example = RandomPromptRecord[1]
##    if forward_or_back_list_item_from_state(State):
##        push_item_onto_back_list(State, forward_or_back_list_item_from_state(State))
##    State['prompt'] = PromptText
##    State['example'] = Example
##    return current_prompt_for_state(State)

def forward_list_for_all_prompts(State):
    Language = State['language']
    AllPrompts = prompts_for_state(State)
    Groups = list(AllPrompts.keys())
    OrderedGroups = order_if_all_numbers_else_permute(Groups)
    return forward_list_for_all_prompts1(OrderedGroups, AllPrompts, Language, State)

def forward_list_for_all_prompts1(OrderedGroups, AllPrompts, Language, State):
    if len(OrderedGroups) == 0:
        return []
    else:
        F = OrderedGroups[0]
        R = OrderedGroups[1:]
        return forward_list_for_prompts_in_group(AllPrompts[F], Language, State) + forward_list_for_all_prompts1(R, AllPrompts, Language, State)

def forward_list_for_prompts_in_group(PromptRecordsForGroup, Language, State):
    return random_permutation(prompt_records_to_forward_list(PromptRecordsForGroup, Language, State))

def prompt_records_to_forward_list(PromptRecordsForGroup, Language, State):
    return [ prompt_record_to_forward_list(X, Language, State) for X in PromptRecordsForGroup ]

def prompt_record_to_forward_list(PromptRecord, Language, State):
    PromptText = PromptRecord[0][Language]
    Canonical = PromptRecord[1]
    Example = PromptRecord[2]
    Multimedia = prompt_record_to_multimedia(PromptRecord, State)
    if not null_multimedia(Multimedia):
        Prompt = Multimedia
    else:
        Prompt = PromptText
    return { 'prompt':Prompt, 'canonical':Canonical, 'example':Example }

def prompt_record_to_multimedia(PromptRecord, State):
    BaseMultimedia = PromptRecord[4]
    if null_multimedia(BaseMultimedia):
        return BaseMultimedia
    else:
        Prefix = state_to_multimedia_prefix(State)
        BaseMultimediaCorrected = change_extension_to_mp3(BaseMultimedia)
        return '<audio src="' + Prefix + BaseMultimediaCorrected + '"/>'

def state_to_multimedia_prefix(State):
    return course_info_for_state(State)['s3prefix'] + State['namespace'] + '/' + State['domain'] + '/'

def null_multimedia(Multimedia):
    if Multimedia == '*no_multimedia*':
        return True
    else:
        return False

def go_back(State):
    if not 'backList' in State or len(State['backList']) == 0:
        return { 'response_to':'back', 'error':'no_previous_prompt' }
    else:
        BackList = State['backList']
        BackItem = BackList[0]
        newBackList = BackList[1:]
        ForwardItem = forward_or_back_list_item_from_state(State)
        push_item_onto_forward_list(State, ForwardItem)
        update_state_from_forward_or_back_list_item(State, BackItem)
        State['backList'] = newBackList
        return merge_dicts(current_prompt_for_state(State), { 'type':'prompt', 'response_to':'back' })

##loaded_flat_interlingua_prompt = {
##    tuple(["zahlenspiel", "zahlenspiel", "lesson_3"]):
##      [{ 1:[ [ { "german":"drei mal vier" }, "zwölf", "zwölf", [], "*no_multimedia*" ],
##             [ { "german":"fünf mal neun" }, "fünf_und_vierzig", "fünf und vierzig", [], "*no_multimedia*" ],
##             [ { "german":"fünf mal sechs" }, "dreißig", "dreißig", [], "*no_multimedia*" ],
##             [ { "german":"vier mal fünf" }, "zwanzig", "zwanzig", [], "*no_multimedia*" ],
##             [ { "german":"zwei mal acht" }, "sechzehn", "sechzehn", [], "*no_multimedia*" ],
##             [ { "german":"zwei mal zwei" }, "vier", "vier", [], "*no_multimedia*" ] ],
##         2:[ [ { "german":"acht mal neun" }, "zwei_und_siebzig", "zwei und siebzig", [], "*no_multimedia*" ],
##             [ { "german":"drei mal acht" }, "vier_und_zwanzig", "vier und zwanzig", [], "*no_multimedia*" ],
##             [ { "german":"sechs mal sechs" }, "sechs_und_dreißig", "sechs und dreißig", [], "*no_multimedia*" ],
##             [ { "german":"sechs mal vier" }, "vier_und_zwanzig", "vier und zwanzig", [], "*no_multimedia*" ],
##             [ { "german":"sieben mal acht" }, "sechs_und_fünfzig", "sechs und fünfzig", [], "*no_multimedia*" ],
##             [ { "german":"sieben mal zwei" }, "vierzehn", "vierzehn", [], "*no_multimedia*" ],
##             [ { "german":"vier mal sieben" }, "acht_und_zwanzig", "acht und zwanzig", [], "*no_multimedia*" ] ] }],

def get_help(State):
    HelpTextAndNItems = help_text_and_number_of_help_items_for_state(State)
    if HelpTextAndNItems:
        ( HelpText, NHelpItems ) = HelpTextAndNItems
        Help = { 'type':'prompt', 'response_to':'help', 'text':HelpText, 'n_help_items':NHelpItems, 'prompt':State['prompt'] }
        State['helpgiven'] = State['helpgiven'] + 1
        return Help
    else:
        return { 'response_to':'help', 'error':'no_help_available' }

##loaded_recorded_help = {
##    tuple(["dante2", "dante2", "nel_mezzo_del_cammin_di_nostra_vita"]):[[ [ "help/12145_161223053529.wav", "Nel mezzo del cammin di nostra vita" ], [ "*no_file*", "MIDWAY upon the journey of our life" ] ]],
##    tuple(["dante2", "dante2", "mi_ritrovai_per_una_selva_oscura"]):[[ [ "help/12146_161223053545.wav", "mi ritrovai per una selva oscura" ], [ "*no_file*", "I found myself within a forest dark," ] ]],
##    tuple(["dante2", "dante2", "ché_la_diritta_via_era_smarrita"]):[[ [ "help/12147_161223054216.wav", "ché la diritta via era smarrita." ], [ "*no_file*", "For the straightforward pathway had been lost." ] ]],

def get_spoken_help(State):
    if tables.loaded_recorded_help and 'namespace' in State:
        Key0 = tuple([ State['namespace'] ])
    else:
        return False
    if Key0 in tables.loaded_recorded_help:
        Table = tables.loaded_recorded_help[Key0]
    else:
        return False
    if 'domain' in State and 'canonical' in State:
        Key = tuple([ State['namespace'], State['domain'], State['canonical'] ])
        if Key in Table:
            return Table[Key]
        else:
            return False
    else:
        return False

## stored_lesson = {
##    tuple(["dante2", "dante2", "lesson_1"]):[{ "namespace":"dante2", "domain":"dante2", "lesson_id":"lesson_1", "short_name":"Inferno I 1-30", "description":"Inferno I 1-30", "help_file":"dante21.html", 

def get_help_file(State):
    if tables.stored_lesson and 'namespace' in State:
        Key0 = tuple([ State['namespace'] ])
    else:
        return False
    if Key0 in tables.stored_lesson:
        Table = tables.stored_lesson[Key0]
    else:
        return False
    if 'domain' in State and 'lesson' in State:
        Key = tuple([ State['namespace'], State['domain'], State['lesson'] ])
        if Key in Table and 'help_file' in Table[Key][0]:
            return Table[Key][0]['help_file']
        else:
            return False
    else:
        return False
    

def wait(State):
    return { 'type':'wait', 'response_to':'wait', 'text':State['prompt'] }

def exit_game(State):
    return { 'type':'exit', 'response_to':'exit' }

def help_text_and_number_of_help_items_for_state(State):
    Strategy = get_help_strategy_for_state(State)
    if Strategy == 'default' or help_already_given_for_current_prompt(State):
        return ( default_help_text_for_state(State), 1 )
    elif Strategy == '2hints':
        return hint_help_text_and_number_of_help_items_for_state(State, 2)
    elif Strategy == '3hints':
        return hint_help_text_and_number_of_help_items_for_state(State, 3)
    else:
        print('*** Error: unknown help strategy: ' + Strategy)
        return False

def get_max_tries_for_state(State):
    CourseInfo = course_info_for_state(State)
    if 'maxtries' in CourseInfo:
        return CourseInfo['maxtries']
    else:
        return 3

def get_help_strategy_for_state(State):
    CourseInfo = course_info_for_state(State)
    if 'helpstrategy' in CourseInfo:
        return CourseInfo['helpstrategy']
    else:
        return 'default'

def help_already_given_for_current_prompt(State):
    if 'helpgiven' in State:
        return State['helpgiven'] > 0
    else:
        State['helpgiven'] = 0
        return False

def hint_help_text_and_number_of_help_items_for_state(State, N):
    CorrectHelpText = default_help_text_for_state(State)
    if N < 2:
        return ( CorrectHelpText, 1 )
    else:
        N1 = N - 1
        IncorrectHelpTexts = random_help_texts_for_state(State, N1, CorrectHelpText)
        AllHelpTexts = random_permutation( [ CorrectHelpText ] + IncorrectHelpTexts )
        return ( output_manager.join_text_list_with_or(AllHelpTexts, State['language'], State['l2']), len(AllHelpTexts) )

def random_help_texts_for_state(State, N, CorrectHelpText):
    AllHelpTexts = all_help_texts_for_state(State).copy()
    if CorrectHelpText in AllHelpTexts:
        AllHelpTexts.remove(CorrectHelpText)
    return n_random_members_of_list(AllHelpTexts, N)

def all_help_texts_for_state(State):
    if 'allHelpTexts' in State:
        return State['allHelpTexts']
    else:
        return []                    

def default_help_text_for_state(State):
    if 'example' in State:
        Help = State['example']
        return Help
    else:
        return False

def get_last_system_utterance(State):
    if 'text_to_repeat' in State:
        Help = { 'type':'repeat', 'response_to':'repeat', 'text':State['text_to_repeat'] }
        return Help
    else:
        return { 'response_to':'repeat', 'error':'no_last_utterance' }

##sent_atom_namespace_lf_l1_text = {
##    tuple(["acht", "german_translation_game", "german_arithmetic", "german"]):[[ [ "acht", "vier plus vier" ], [ "acht", "zwei plus sechs" ] ]],
##    tuple(["achtundachtzig", "german_translation_game", "german_arithmetic", "german"]):[[ [ "dummy_incorrect", "Incorrect version of: dummy_text" ] ]],
##    tuple(["achtunddreißig", "german_translation_game", "german_arithmetic", "german"]):[[ [ "dummy_incorrect", "Incorrect version of: dummy_text" ] ]],
##    (...)
##    }

def match(String, State):
    Key0 = tuple([State['namespace']])
    Key = tuple([ String, State['namespace'], State['domain'], State['language'] ])
    if ( Key0 in tables.sent_atom_namespace_lf_l1_text and Key in tables.sent_atom_namespace_lf_l1_text[Key0] ):
        Possibilities = tables.sent_atom_namespace_lf_l1_text[Key0][Key][0]
        CurrentCanonical = State['canonical']
        Match = match_possibilities_against_canonical(Possibilities, CurrentCanonical)
        MatchStructure = { 'match':Match }
        if Match == 'yes':
            scores.score_correct_match(State)
        else:
            State['attempts'] = State['attempts'] + 1
    else:
        MatchStructure = { 'match':'no' }
        State['attempts'] = State['attempts'] + 1
    return merge_dicts( MatchStructure,
                        { 'type':'match_response', 'response_to':'match',
                          'match_string':String, 'prompt':State['prompt'],
                          'attempts':State['attempts'], 'max_tries':get_max_tries_for_state(State),
                          'feedback':State['feedback'], 'helpgiven':State['helpgiven']}
                        )

# ----------------------------------------

##course_info = {
##    tuple(["german_arithmetic", "german_translation_game"]):[{ "namespace":"german_translation_game", "name":"german_arithmetic", "client":"translation_game_client", "feedback":"default", "l2":"german", "languages":[ "german" ], "endmessage":"End of lesson", "users":[ "any" ], "grammarlevel":"per_course", "reccase":"initialCapital", "acceptbonus":100, "autoadvance":"yes", "canmoveforward":"yes", "canmoveback":"yes", "showhelp":[ 1, "first" ], "startscore":100, "maxtries":3, "rejectpenalty":2, "skippenalty":5, "plainbadge":0, "bronzebadge":0, "silverbadge":90, "goldbadge":100 }],
##    tuple(["german_arithmetic2", "german_translation_game"]):[{ "namespace":"german_translation_game", "name":"german_arithmetic2", "client":"translation_game_client", "feedback":"default", "l2":"german", "languages":[ "german" ], "endmessage":"End of lesson", "users":[ "any" ], "grammarlevel":"per_course", "reccase":"initialCapital", "acceptbonus":100, "autoadvance":"yes", "canmoveforward":"yes", "canmoveback":"yes", "showhelp":[ 1, "first" ], "startscore":100, "maxtries":3, "rejectpenalty":2, "skippenalty":5, "plainbadge":0, "bronzebadge":0, "silverbadge":90, "goldbadge":100 }]
##}

def valid_namespace_domain_and_language(Namespace, Domain, Language):
    CourseInfo = course_info_for_namespace_and_domain(Namespace, Domain)
    if CourseInfo:
        return Language in CourseInfo['languages']
    else:
        return False
    
def get_available_namespaces_domains_and_l1s():
    return [ [ Key0[0], Key[0], Language ]
              for Key0 in tables.course_info
              for Key in tables.course_info[Key0]
              for Language in tables.course_info[Key0][Key][0]['languages']
            ]

##stored_lesson = {
##    tuple(["german_translation_game", "german_arithmetic", "addition"]):[{ "namespace":"german_translation_game", "domain":"german_arithmetic", "lesson_id":"addition", "short_name":"Addition", "description":"(no description)", "requirespassword":"no" }],

def get_next_lesson(State):
    if not 'namespace' in State or not 'domain' in State or not 'lesson' in State:
        return False
    else:
        Key0 = tuple([State['namespace']])
    if not ( Key0 in tables.stored_lesson ):
        return False
    else:
        StoredLessonTuples = tables.stored_lesson[Key0]
        Lessons = [ Tuple[2] for Tuple in StoredLessonTuples if Tuple[0] == State['namespace'] and Tuple[1] == State['domain'] ]
        return next_lesson_from_list(Lessons, State['lesson'])

def next_lesson_from_list(Lessons, Lesson):
    if len(Lessons) < 1:
        return False
    elif next_lesson_from_list1(Lessons, Lesson):
        return next_lesson_from_list1(Lessons, Lesson)
    # If we're at the end, go back to the beginning
    else:
        return Lessons[0]

def next_lesson_from_list1(Lessons, Lesson):
    if len(Lessons) > 1 and Lessons[0] == Lesson:
        return Lessons[1]
    elif len(Lessons) > 2:
        return next_lesson_from_list1(Lessons[1:], Lesson)
    else:
        return False

def valid_lesson_in_state(State, Lesson):
    if not 'namespace' in State:
        return False
    else:
        Key0 = tuple([State['namespace']])
    if not ( Key0 in tables.stored_lesson ):
        return False
    else:
        StoredLessons = tables.stored_lesson[Key0]
    if 'domain' in State:
        return tuple([State['namespace'], State['domain'], Lesson]) in StoredLessons
    else:
        return False

def number_of_lessons_in_state(State):
    if not 'namespace' in State or not 'domain' in State:
        return 0
    else:
        Key0 = tuple([State['namespace']])
    if not ( Key0 in tables.stored_lesson ):
        return 0
    else:
        StoredLessons = tables.stored_lesson[Key0]
        return len( [ Key for Key in StoredLessons if Key[0] == State['namespace'] and Key[1] == State['domain'] ] )
    
##stored_lesson = {
##    tuple(["zahlenspiel", "zahlenspiel", "lesson_1"]):[{ "namespace":"zahlenspiel", "domain":"zahlenspiel", "lesson_id":"lesson_1", "short_name":"addition", "description":"addition", "requirespassword":"no" }],
##    tuple(["zahlenspiel", "zahlenspiel", "lesson_2"]):[{ "namespace":"zahlenspiel", "domain":"zahlenspiel", "lesson_id":"lesson_2", "short_name":"subtraktion", "description":"subtraktion", "requirespassword":"no" }],
##    tuple(["zahlenspiel", "zahlenspiel", "lesson_3"]):[{ "namespace":"zahlenspiel", "domain":"zahlenspiel", "lesson_id":"lesson_3", "short_name":"multiplikation", "description":"multiplikation", "requirespassword":"no" }],
##    tuple(["zahlenspiel", "zahlenspiel", "lesson_4"]):[{ "namespace":"zahlenspiel", "domain":"zahlenspiel", "lesson_id":"lesson_4", "short_name":"division", "description":"division", "requirespassword":"no" }]
##}

def get_available_lessons(State):
    if ( not 'namespace' in State ) or ( not 'domain' in State ):
        Lessons = []
    else:
        Lessons = [ Key[2] for Key in tables.stored_lesson[tuple([State['namespace']])] if Key[1] == State['domain'] ]
    return { 'type':'lessons', 'response_to':'get_lessons', 'lessons':Lessons }

def get_available_lesson_names(State):
    if ( not 'namespace' in State ) or ( not 'domain' in State ):
        Lessons = []
    else:
        Table = tables.stored_lesson[tuple([State['namespace']])]
        Lessons = [ Table[Key][0]['short_name'] for Key in Table if Key[1] == State['domain'] ]
    return { 'type':'lessons', 'response_to':'get_lessons', 'lessons':Lessons }

def name_for_lesson(Lesson, State):
    if ( not 'namespace' in State ) or ( not 'domain' in State ):
        return 'error'
    else:
        Table = tables.stored_lesson[tuple([State['namespace']])]
        Key = tuple([State['namespace'], State['domain'], Lesson])
        if not Key in Table:
            return 'error'
        else:
            return Table[Key][0]['short_name']

def lesson_for_name(LessonName, State):
    if ( not 'namespace' in State ) or ( not 'domain' in State ):
        return 'error'
    else:
        Table = tables.stored_lesson[tuple([State['namespace']])]
        for Key in Table:
            LessonData = Table[Key][0]
            if 'lesson_id' in LessonData and 'short_name' in LessonData and LessonData['short_name'] == LessonName:
                return LessonData['lesson_id']
        return False   

# ----------------------------------------

def import_course_info_into_state(State):
    CourseInfo = course_info_for_state(State)
    State['l2'] = CourseInfo['l2']
    State['feedback'] = CourseInfo['feedback']

def course_info_for_state(State):
    Namespace = State['namespace']
    Domain = State['domain']
    return course_info_for_namespace_and_domain(Namespace, Domain)

def course_info_for_namespace_and_domain(Namespace, Domain):
    Key0 = tuple([Namespace])
    if not ( Key0 in tables.course_info ):
        return False
    CoursesForNamespace = tables.course_info[Key0]
    Key = tuple([Domain, Namespace])
    if not ( Key in CoursesForNamespace ):
        return False
    return CoursesForNamespace[Key][0]

def prompts_for_state(State):
    [Namespace, Domain, Lesson] = [State['namespace'], State['domain'], State['lesson']]
    return tables.loaded_flat_interlingua_prompt[tuple([Namespace])][tuple([Namespace, Domain, Lesson])][0]

def match_possibilities_against_canonical(Possibilities, Canonical):
    for Record in Possibilities:
        if Record[0] == Canonical:
            return 'yes'
    return 'no'

def update_state_from_forward_or_back_list_item(State, Item):
    ( Prompt, Example, Canonical ) = ( Item['prompt'], Item['example'], Item['canonical'] )
    State['prompt'] = Prompt
    State['example'] = Example
    State['canonical'] = Canonical
    State['attempts'] = 0
    State['helpgiven'] = 0
    scores.start_new_prompt(State)
    log.print_log_message(['set_prompt', { 'prompt':Prompt, 'canonical':Canonical }])

def forward_or_back_list_item_from_state(State):
    if 'prompt' in State and 'example' in State and 'canonical' in State:
        Item = {}
        Item['prompt'] = State['prompt'] 
        Item['example'] = State['example']
        Item['canonical'] = State['canonical']
        return Item
    else:
        return False

def push_item_onto_back_list(State, Item):
    if 'backList' in State:
        BackList = State['backList']
    else:
        BackList = []
    State['backList'] = [Item] + BackList

def push_item_onto_forward_list(State, Item):
    if 'forwardList' in State:
        ForwardList = State['forwardList']
    else:
        ForwardList = []
    State['forwardList'] = [Item] + ForwardList

def current_prompt_for_state(State):
    Prompt = { 'text':State['prompt'] }
    return Prompt

# Robust matching

def robust_process_string_for_call(String, State):
    MatchResults = lgm.match_string(String, 1, State['namespace'], State['domain'])
    if len(MatchResults) > 0 and plausible_match(MatchResults[0]):
        #return correct_orthography_in_match_string(MatchResults[0]['matched'])
        return MatchResults[0]['matched']
    else:
        return String

def robust_match_string(String, State, N):
    return lgm.match_string(String, N, State['namespace'], State['domain'])

# Third try: we do it all on the compiler side.
# Add more keys to sent_atom_namespace_lf_l1_text to take account of regularised text

##def add_regularised_keys_to_sent_atom_namespace_lf_l1_text(Namespace, Domain):
##    Key0 = tuple([Namespace])
##    if not Key0 in tables.sent_atom_namespace_lf_l1_text:
##        print('*** Error: sent_atom_namespace_lf_l1_text not found for {namespace}'.format(namespace=Namespace))
##        return False
##    Table = tables.sent_atom_namespace_lf_l1_text[Key0]
##    NewEntries = {}
##    for Key in Table:
##        String = Key[0]
##        RegularisedString = lgm_regularise.regularise_string(String, Namespace, Domain)
##        if String != RegularisedString:
##            RegularisedKey = tuple([ RegularisedString, Key[1], Key[2], Key[3] ])
##            NewEntries[RegularisedKey] = Table[Key]
##            #print('--- Added key {key}'.format(key=Key))
##    if len(NewEntries) > 0:
##        NewTable = merge_dicts(Table, NewEntries)
##        tables.sent_atom_namespace_lf_l1_text[Key0] = NewTable
##        print('--- {n} regularised keys added to sent_atom_namespace_lf_l1_text table'.format(n=len(NewEntries)))

# The following is now handled more generally by adding regularised keys, immediately above.
# The match string has split up words with apostrophes.
# So e.g. "l'allemand" becomes "l' allemand" and we need to change it back again.
#def correct_orthography_in_match_string(Str):
#    return Str.replace("' ", "'")

# Initial definition (really we should use ML)
#
# We say it's a plausible match if
#   a) we've got at least one high-scoring word in the trace, or
#   b) the total match score is high enough
#
# >>> lgm.match_string('aide moi obi-wan kenobi', 2, 'jeu_des_animaux', 'jeu_des_animaux')
# [{'canonical': 'help', 'rule': 'jeu_des_animaux__jeu_des_animaux__12-help', 'matched': 'aide moi',
#   'tf_idf_score': 1.5, 'score': 1.5,
#   'trace': [['aide', 1.0], ['moi', 0.5], ['obi-wan', 'skipped'], ['kenobi', 'skipped'], ['context_bonus', 0.0]],
#   'tf_idf_penalizing_unmatched': 1.1400000000000001},
#  {'canonical': 'repeat', 'rule': 'jeu_des_animaux__jeu_des_animaux__18-repeat', 'matched': 'redis moi',
#   'tf_idf_score': 0.5, 'score': 0.32,
#   'trace': [['redis', 'skipped'], ['moi', 0.5], ['aide', 'skipped'], ['obi-wan', 'skipped'], ['kenobi', 'skipped'],
#   ['context_bonus', 0.0]], 'tf_idf_penalizing_unmatched': -0.22000000000000003}]

def plausible_match(MatchResultsItem):
    for TraceItem in MatchResultsItem['trace']:
        if is_number(TraceItem[1]) and TraceItem[1] > 0.1:
            return True
    if MatchResultsItem['tf_idf_penalizing_unmatched'] > 0.2:
        return True
    else:
        return False

# Checking tables are loaded

def check_tables_are_loaded():
    tables.check_tables_are_loaded()
    lgm_tables.check_tables_are_loaded()

# Utilities

def merge_dicts(X, Y):
    return { **X, **Y }

def order_if_all_numbers_else_permute(List):
    if all_numbers_list(List):
        return sorted(List)
    else:
        return random_permutation(List)

def all_numbers_list(List):
    for X in List:
        if not is_number(X):
            return False
    return True

def is_number(X):
    return isinstance(X, (int, float, complex))

def n_random_members_of_list(List, N):
    if N < 1:
        return []
    elif len(List) == 0:
        return []
    else:
        X = random_member(List)
        List.remove(X)
        return [ X ] + n_random_members_of_list(List, N-1)

def random_permutation(List):
    if len(List) < 2:
        return List
    else:
        X = random_member(List)
        List.remove(X)
        return [ X ] + random_permutation(List)

def random_member(List):
    return random.choice(List)

def change_extension_to_mp3(File):
    FileComponents = File.split('.')
    if len(FileComponents) > 1:
        Base = '.'.join(FileComponents[0:-1])
    else:
        Base = File
    return Base + '.mp3'

