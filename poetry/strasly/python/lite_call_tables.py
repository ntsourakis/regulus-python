
import gzip, pickle

##all_data = {
##"available_l1s_for_namespace":available_l1s_for_namespace,
##"course_info":course_info,
##"stored_lesson":stored_lesson,
##"loaded_flat_interlingua_prompt":loaded_flat_interlingua_prompt,
##"accept_bonus_for_namespace_and_course":accept_bonus_for_namespace_and_course,
##"sent_atom_namespace_lf_l1_text":sent_atom_namespace_lf_l1_text
##}

available_l1s_for_namespace = {}
course_info = {}
stored_lesson = {}
loaded_flat_interlingua_prompt = {}
accept_bonus_for_namespace_and_course = {}
sent_atom_namespace_lf_l1_text = {}
loaded_recorded_help = {}

def check_tables_are_loaded():
    global loaded_flat_interlingua_prompt
    global sent_atom_namespace_lf_l1_text
    if loaded_flat_interlingua_prompt == {}:
        print('*** Warning: CALL table loaded_flat_interlingua_prompt has not been initialised')
    if sent_atom_namespace_lf_l1_text == {}:
        print('*** Warning: CALL table sent_atom_namespace_lf_l1_text has not been initialised')

def load_data(tables_file):
    global available_l1s_for_namespace
    global course_info
    global stored_lesson
    global loaded_flat_interlingua_prompt
    global accept_bonus_for_namespace_and_course
    global sent_atom_namespace_lf_l1_text
    global loaded_recorded_help
    
    f = gzip.open(tables_file, 'rb')
    all_data = pickle.load(f)
    f.close()
    print('Loaded CALL table data from {}'.format(tables_file))

    NamespaceEtc = namespace_domain_etc_from_all_data(all_data)

    if NamespaceEtc:
        Key = tuple([NamespaceEtc['namespace']])
        available_l1s_for_namespace[Key] = component(all_data, 'available_l1s_for_namespace')
        course_info[Key] = component(all_data, 'course_info')
        stored_lesson[Key] = component(all_data, 'stored_lesson')
        loaded_flat_interlingua_prompt[Key] = component(all_data, 'loaded_flat_interlingua_prompt')
        accept_bonus_for_namespace_and_course[Key] = component(all_data, 'accept_bonus_for_namespace_and_course')
        sent_atom_namespace_lf_l1_text[Key] = component(all_data, 'sent_atom_namespace_lf_l1_text')
        loaded_recorded_help[Key] = component(all_data, 'loaded_recorded_wavfile_lite')
        return NamespaceEtc
    else:
        return False

##course_info = {
##    tuple(["zahlenspiel", "zahlenspiel"]):[{ "namespace":"zahlenspiel",
##                                             "name":"zahlenspiel",
##                                             "client":"translation_game_client",
##                                             "invocation":"zahlenspiel",
##                                             "feedback":"default",
##                                             "l2":"german",
##                                             "languages":[ "german" ]
##                                             (...)
##}

def namespace_domain_etc_from_all_data(all_data):
    CourseInfo = component(all_data, 'course_info')
    if CourseInfo:
        Dict = list(CourseInfo.values())[0][0]
        return { 'namespace':Dict['namespace'],
                 'domain':Dict['name'],
                 'l2':Dict['l2'],
                 'l1':Dict['languages'][0]
                 }
    else:
        return False

def component(all_data, component_name):
    if all_data == 'null':
        print('*** Error: no data loaded')
        return False
    elif component_name in all_data:
        return all_data[component_name]
    else:
        print('*** Warning: no table called {}'.format(component_name))
        return False

