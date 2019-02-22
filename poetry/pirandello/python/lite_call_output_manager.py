#!/usr/bin/python

import pirandello.python.lite_call_tables as tables

import pirandello.python.lite_call_english as english
import pirandello.python.lite_call_french as french
import pirandello.python.lite_call_german as german

# Turn abstract actions into strings

def abstract_call_action_to_action(AbstractAction, L1, L2):
    if 'error' in AbstractAction:
        return abstract_error_to_action(AbstractAction, L1, L2)
    elif not 'type' in AbstractAction or not 'response_to' in AbstractAction:
        return abstract_error_to_action({'error':'internal_error'}, L1, L2)
    else:
        Type = AbstractAction
        ResponseTo = AbstractAction['response_to']
        
    if ResponseTo == 'match':
        return match_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'repeat':
        return repeat_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'wait':
        return wait_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'exit':
        return exit_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'next':
        return next_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'auto_next':
        return auto_next_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'back':
        return back_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'help':
        return help_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'get_lessons':
        return get_lessons_to_action(AbstractAction, L1, L2)
    elif ResponseTo == 'set_lesson':
        return set_lesson_to_action(AbstractAction, L1, L2)
    else:
        return abstract_error_to_action({'error':'internal_error'}, L1, L2)

def dont_understand_action(L1, L2, State):
    Main = l(L2, 'I don\'t understand')
    Invocation = invocation_name(State)
    Text = '{invocation}. {main}'.format(invocation=Invocation, main=Main)
    return { 'text':Text, 'auto_next':'no', 'end':'no' }

def prepend_invocation_name_to_action_text(Action, State):
    Main = Action['text']
    Invocation = invocation_name(State)
    Action['text'] = '{invocation}. {main}'.format(invocation=Invocation, main=Main)
    return Action

# Correct actions

# We do an auto-next
#    after a successful match,
#    or after an unsuccessful match if we have used up all our tries
def match_to_action(AbstractAction, L1, L2):
    if AbstractAction['match'] == 'yes':
        # If we're doing a mini-dialogue, we don't echo back the match string
        if 'feedback' in AbstractAction and AbstractAction['feedback'] == 'alexa_minidialogue':
            Text = l(L2, 'yes')
        else:
            Pattern = l(L2, 'yes {string}')
            Text = Pattern.format( string=AbstractAction['match_string'] )
        return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'auto_next', 'end':'no' }
    elif ( 'attempts' in AbstractAction and 'max_tries' in AbstractAction and
           AbstractAction['attempts'] >= AbstractAction['max_tries'] ):
        Pattern = l(L2, 'no {string}')
        Text = Pattern.format( string=AbstractAction['match_string'] )
        return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'auto_next', 'end':'no' }
    else:
        Pattern = l(L2, 'no {string} {prompt}')
        Prompt0 = AbstractAction['prompt']
        Prompt = maybe_wrap_prompt(Prompt0, L1, L2)
        Text = Pattern.format( string=AbstractAction['match_string'], prompt=Prompt )
        return { 'text':Text, 'text_to_repeat':Prompt, 'auto_next':'no', 'end':'no' }

def exit_to_action(AbstractAction, L1, L2):
    Text = l(L2, 'Exit')
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'yes' }

def repeat_to_action(AbstractAction, L1, L2):
    Text0 = AbstractAction['text']
    Text = l(L2, 'Repeat. {text}').format(text=Text0)
    return { 'text':Text, 'text_to_repeat':Text0, 'auto_next':'no', 'end':'no' }

def wait_to_action(AbstractAction, L1, L2):
    Text0 = AbstractAction['text']
    Text1 = maybe_wrap_prompt(Text0, L1, L2)
    Text = l(L2, 'Waiting. {prompt}').format(prompt=Text1)
    return { 'text':Text, 'text_to_repeat':Text1, 'auto_next':'no', 'end':'no' }

def next_to_action(AbstractAction, L1, L2):
    Text0 = AbstractAction['text']
    Text1 = maybe_wrap_prompt(Text0, L1, L2)
    Text = l(L2, 'Next: {prompt}').format(prompt=Text1)
    return { 'text':Text, 'text_to_repeat':Text1, 'auto_next':'no', 'end':'no' }

# For auto-next, we don't echo 'next' at the beginning
def auto_next_to_action(AbstractAction, L1, L2):
    Text0 = AbstractAction['text']
    Text1 = maybe_wrap_prompt(Text0, L1, L2)
    Text = l(L2, '{prompt}').format(prompt=Text1)
    return { 'text':Text, 'text_to_repeat':Text1, 'auto_next':'no', 'end':'no' }

def back_to_action(AbstractAction, L1, L2):
    Text0 = AbstractAction['text']
    Text1 = maybe_wrap_prompt(Text0, L1, L2)
    Text = l(L2, 'Back: {prompt}').format(prompt=Text1)
    return { 'text':Text, 'text_to_repeat':Text1, 'auto_next':'no', 'end':'no' }

def help_to_action(AbstractAction, L1, L2):
    Text0 = AbstractAction['text']
    Prompt0 = AbstractAction['prompt']
    Prompt = maybe_wrap_prompt(Prompt0, L1, L2)
    if 'n_help_items' in AbstractAction and AbstractAction['n_help_items'] == 1:
        Text = l(L2, 'Help: the answer is {text}. {prompt} (then continue)').format(text=Text0, prompt=Prompt)
        return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'auto_next', 'end':'no' }
    else:
        Text = l(L2, 'Help: the answer is {text}. {prompt}').format(text=Text0, prompt=Prompt)
        return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'no' }

def get_lessons_to_action(AbstractAction, L1, L2):
    Lessons = join_text_list_with_or(AbstractAction['lessons'], L1, L2)
    Text = l(L2, 'Lessons: {lessons}').format(lessons=Lessons)
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'no' }

def set_lesson_to_action(AbstractAction, L1, L2):
    Lesson = AbstractAction['lesson']
    Text0 = AbstractAction['text']
    Text1 = maybe_wrap_prompt(Text0, L1, L2)
    if 'number_of_lessons' in AbstractAction and AbstractAction['number_of_lessons'] == 1:
        Text = l(L2, '{prompt}').format(prompt=Text1)
    else:
        Text = l(L2, 'Lesson: {lesson}. {prompt}').format(lesson=Lesson, prompt=Text1)
    return { 'text':Text, 'text_to_repeat':Text1, 'auto_next':'no', 'end':'no' }

# Error actions

def abstract_error_to_action(AbstractAction, L1, L2):
    Error = AbstractAction['error']
    if Error == 'unknown_lesson':
        return unknown_lesson_to_action(AbstractAction, L1, L2)
    elif Error == 'no_more_prompts_in_lesson':
        return no_more_prompts_in_lesson_to_action(AbstractAction, L1, L2)
    elif Error == 'no_previous_prompt':
        return no_previous_prompt_to_action(AbstractAction, L1, L2)
    elif Error == 'no_help_available':
        return no_help_available_to_action(AbstractAction, L1, L2)
    elif Error == 'no_last_utterance':
        return no_last_utterance_to_action(AbstractAction, L1, L2)
    else:
        return internal_error_to_action(AbstractAction, L1, L2)
    
def unknown_lesson_to_action(AbstractAction, LL1, L2):
    Text = l(L2, 'Unknown lesson')
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'no' }

def no_more_prompts_in_lesson_to_action(AbstractAction, L1, L2):
    Text = l(L2, 'At end of lesson {score} {max_possible_score}').format(score=AbstractAction['score'],
                                                                         max_possible_score=AbstractAction['max_possible_score'])
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'next_lesson', 'end':'no' }

def no_previous_prompt_to_action(AbstractAction, L1, L2):
    Text = l(L2, 'At beginning of lesson')
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'no' }

def no_help_available_to_action(AbstractAction, L1, L2):
    Text = l(L2, 'No help is available')
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'no' }

def no_last_utterance_to_action(AbstractAction, L1, L2):
    Text = l(L2, 'Nothing to repeat')
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'no' }

def internal_error_to_action(AbstractAction, L1, L2):
    Text = l(L2, 'Something went wrong')
    return { 'text':Text, 'text_to_repeat':Text, 'auto_next':'no', 'end':'yes' }

def join_text_list_with_or(List, L1, L2):
    Length = len(List)
    if Length == 0:
        return ''
    elif Length == 1:
        return List[0]
    elif Length == 2:
        return l(L2, '{t1} or {t2}').format(t1=List[0], t2=List[1])
    else:
        return l(L2, '{t1}, {t2}').format(t1=List[0], t2=join_text_list_with_or(List[1:], L1, L2))

##course_info = {
##    tuple(["number_game", "number_game"]):[{ "namespace":"number_game",
##                                             "name":"number_game",
##                                             "client":"translation_game_client",
##                                             "alexa":"yes",
##                                             "invocation":"number game",
##                                             (...)}]
##}

def invocation_name(State):
    Key0 = tuple([State['namespace']])
    Key = tuple([State['namespace'], State['domain']])
    return tables.course_info[Key0][Key][0]['invocation']

## We need to wrap the prompt in a <voice> and <lang> tag if the L1 is different from the L2
## and the L1 isn't 'mixed', meaning the prompt is already formatted as a piece of SSML.
##
## Example of wrapped output:
## <voice name="Celine"><lang xml:lang="fr-FR">Bienvenue à Car-Fu</lang></voice>

def maybe_wrap_prompt(Prompt, L1, L2):
    if L1 == L2 or L1 == 'mixed':
        return Prompt
    else:
        ( LangId, Voice) = language_id_and_default_voice_for_language(L1)
        FormatString = '<voice name="{voice}"><lang xml:lang="{lang_id}">{prompt}</lang></voice>'
        return FormatString.format(voice=Voice, lang_id=LangId, prompt=Prompt)

## The following voices are supported for their respective languages:
##
## English, American (en-US): Ivy, Joanna, Joey, Justin, Kendra, Kimberly, Matthew, Salli
## English, Australian (en-AU): Nicole, Russell
## English, British (en-GB): Amy, Brian, Emma
## English, Indian (en-IN): Aditi, Raveena
## German (de-DE): Hans, Marlene, Vicki
## Spanish, Castilian (es-es): Conchita, Enrique
## Italian (it-IT): Carla, Giorgio
## Japanese (ja-JP): Mizuki, Takumi
## French (fr-FR): Celine, Lea, Mathieu

def language_id_and_default_voice_for_language(L1):
    Table = {'english':['en-GB', 'Amy'],
             'german':['de-DE', 'Marlene'],
             'spanish':['es-ES', 'Conchita'],
             'italian':['it-IT', 'Carla'],
             'japanese':['ja-JP', 'Mizuki'],
             'french':['fr-FR', 'Celine']
             }
    if L1 in Table:
        return Table[L1]
    else:
        print('Unsupported TTS prompt language: {l1}'.format(l1=L1))
        return False

def l(L2, Id):
    if L2 == 'german':
        Table = german.german_strings()
        Result0 = lookup_from_language_table(Table, L2, Id)
    elif L2 == 'english':
        Table = english.english_strings()
        Result0 = lookup_from_language_table(Table, L2, Id)
    elif L2 == 'french':
        Table = french.french_strings()
        Result0 = lookup_from_language_table(Table, L2, Id)
    else:
        Result0 = 'Unsupported language: ' + L2
    return substitute_system_dirs_in_string(Result0)

def lookup_from_language_table(Table, L1, Id):
    if Id in Table:
        return Table[Id]
    else:
        return 'Undefined string: ' + Id

def substitute_system_dirs_in_string(String):
    return String.replace("SYSTEM_AUDIO_DIR", system_audio_dir())

def system_audio_dir():
    return "https://s3-eu-west-1.amazonaws.com/timissco/echo/babeldr/english"


