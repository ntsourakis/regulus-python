#!/usr/bin/python

def max_possible_score_per_prompt():
    return 5

def penalty_for_help():
    return 2

def penalty_for_incorrect_answer():
    return 1

def start_new_prompt(State):
    if not 'max_possible_score' in State:
        State['max_possible_score'] = 0
        State['score'] = 0
    State['max_possible_score'] = State['max_possible_score'] + max_possible_score_per_prompt()

def score_correct_match(State):
    Max = max_possible_score_per_prompt()
    if 'attempts' in State:
        IncorrectPenalty = State['attempts'] * penalty_for_incorrect_answer()
    else:
        IncorrectPenalty = 0
    if 'helpgiven' in State and State['helpgiven'] > 0:
        HelpPenalty = penalty_for_help()
    else:
        HelpPenalty = 0
    Score = max([Max - IncorrectPenalty - HelpPenalty, 0])
    State['score'] = State['score'] + Score

    
