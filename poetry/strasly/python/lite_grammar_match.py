#!/usr/bin/python

import strasly.python.lite_grammar_match_tables as lgm_tables
import strasly.python.lite_grammar_match_parameters as parameters
import strasly.python.lite_grammar_match_regularise as regularise
import strasly.python.wagnerfischer as w

# TOP-LEVEL CALLS

# Match a string with a context
def match_string(InputString, NReturned, Namespace, Domain):
    Context = ''
    return match_string_with_context(InputString, Context, NReturned, Namespace, Domain)

# Match a string
def match_string_with_context(InputString, Context, NReturned, Namespace, Domain):
    NShortlist = 13
    InputStringAndContext = (InputString, Context)
    return match_string1(InputStringAndContext, NShortlist, NReturned, Namespace, Domain)

# Match a string, specifying the length of the shortlist
def match_string1(InputStringAndContext, NShortlist, NReturned, Namespace, Domain):
    Words = regularise.convert_input_and_context_to_words_list(InputStringAndContext, Namespace, Domain)
    #RegularisedWordsAtom = " ".join(Words)
    RegularisedWordsAtom = regularise.convert_words_list_to_words_atom(Words)
    return match_string2(Words, RegularisedWordsAtom, Namespace, Domain, NShortlist)[:NReturned]

# ======================================================================

def match_string2(WordsAndContext, WordsAtom, Namespace, Domain, N):
    BestRuleIdsWithInfo = tf_idf_phase(WordsAndContext[0], Namespace, Domain, N)
    return dp_phase(BestRuleIdsWithInfo, WordsAndContext, WordsAtom, Namespace, Domain)

# ======================================================================

# TF-IDF PROCESSING
#
# Use tf-idf information to create a shortlist of candidate rule-ids.
# Each item in the shortlist is a pair (RuleId, Score) where RuleId is the rule-id in question
# Score is the tf-idf score

def tf_idf_phase(Words, Namespace, Domain, LengthOfShortlist):
    Pairs = rule_id_score_pairs_for_words(Words, Namespace, Domain)
    RuleIds = rule_ids_in_rule_id_score_pairs(Pairs)
    return order_rule_ids_by_score(RuleIds, Words, Pairs)[:LengthOfShortlist]

def rule_id_score_pairs_for_words(Words, Namespace, Domain):
    return [ rule_id_score_pair_for_word_and_rule_id(Word, Namespace, Domain, RuleIdAndTfScore)
             for Word in Words
             for RuleIdAndTfScore in rules_for_word(Word, Namespace, Domain) ]

def rule_id_score_pair_for_word_and_rule_id(Word, Namespace, Domain, RuleIdAndTfScore):
    [ RuleId, TfScore ] = RuleIdAndTfScore
    IdfScore = idf_score_for_word(Word, Namespace, Domain)
    Score = combine_tf_and_idf_scores(TfScore, IdfScore)
    Score1 = add_bonus_for_low_scoring_rule(RuleId, Namespace, Domain, Score)
    return [RuleId, Score1]
    
# rules_for_word = {
#     tuple(["abondamment", "babeldr", "abdominal"]):[1, [ { "*-":[ "babeldr__abdominal__2360-suez-vous plus que d'habitude ?", 0.020833333333333332 ] } ]],

def rules_for_word(Word, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.rules_for_word:
        Table = lgm_tables.rules_for_word[Key0]
    else:
        return []
    Key = tuple([Word, Namespace, Domain])
    if Key in Table:
        [Freq, RuleAndScoreTerm] = Table[Key]
        return [ entry["*-"] for entry in RuleAndScoreTerm ]
    else:
        return []

def rule_ids_in_rule_id_score_pairs(Pairs):
    RuleIdsList = [ Pair[0] for Pair in Pairs ]
    return list(set(RuleIdsList))

def order_rule_ids_by_score(RuleIds, InputWords, Pairs):
    ScoredRuleIdsWithInfo = [ score_rule_id(RuleId, InputWords, Pairs) for RuleId in RuleIds ]
    return sorted(ScoredRuleIdsWithInfo, key=lambda x: x[1], reverse=True)

def score_rule_id(RuleId, InputWords, Pairs):
    Score = sum([ Pair[1] for Pair in Pairs if Pair[0] == RuleId ])
    return (RuleId, Score)

# ======================================================================

# DP PROCESSING
# 
# Do DP parsing to get matches between each candidate rule and the list of associated words
# Reorder the list based on the matching score

def dp_phase(BestRuleIdsWithInfo, Words, WordsAtom, Namespace, Domain):
    Results0 = rule_id_word_pairs_to_results(BestRuleIdsWithInfo, Words, Namespace, Domain)
    return sort_match_results_by_score(Results0, Namespace, Domain, WordsAtom)

def rule_id_word_pairs_to_results(RuleIdsWithInfo, Words, Namespace, Domain):
    return [ rule_id_word_pair_to_result(RuleIdWithInfo, Words, Namespace, Domain) for
             RuleIdWithInfo in RuleIdsWithInfo ]

def rule_id_word_pair_to_result(RuleIdWithInfo, Words, Namespace, Domain):
    (RuleId, TfIdfScore) = RuleIdWithInfo
    if parameters.rescoring_strategy == 'none':
        Canonical = rule_id_to_canonical(RuleId, Namespace, Domain)
        return { 'canonical':Canonical, 'rule':RuleId, 'matched':'no_match',
                 'tf_idf_score':TfIdfScore, 'score':TfIdfScore, 'trace':[] }
    else:
        (MatchedSentence, Canonical, Score, Trace) = tf_idf_parse_rule(RuleId, Words, Namespace, Domain)
        MatchedSentenceAtom = " ".join(MatchedSentence)
        return { 'canonical':Canonical, 'rule':RuleId, 'matched':MatchedSentenceAtom,
                 'tf_idf_score':TfIdfScore, 'score':Score, 'trace':Trace }

##tuple(["babeldr_eng2__abdominal__1774-Do you have period pains?"]):
##          [{ "*-->":[ { "*:":[ "unit", [ { "*/":[ "unit", [ "Do", "you", "have", "period", "pains?" ] ] } ] ] },
##                      { "*or":[ [ { "*,":[ "babeldr_eng2__abdominal__do_you_have_or_suffer_from", { "*,":[ [ "period" ], [ "pains" ] ] } ] },
##                       { "*,":[ "babeldr_eng2__abdominal__do_you_have_or_suffer_from", { "*,":[ "babeldr_eng2__abdominal__stomach_pain",
##                       { "*or":[ [ { "*,":[ [ "during" ], { "*,":[ [ "your" ], [ "period" ] ] } ] }, { "*,":[ [ "when" ], { "*,":[ [ "you" ], { "*,":[ [ "are" ],
##                       { "*,":[ [ "having" ], { "*,":[ [ "your" ], [ "period" ] ] } ] } ] } ] } ] },
##                       { "*,":[ [ "at" ], { "*,":[ [ "that" ], { "*,":[ [ "time" ], { "*,":[ [ "of" ], { "*,":[ [ "the" ], [ "month" ] ] } ] }
##                                                                 ] } ] } ] } ] ] } ] } ] } ] ] } ] }]

# And here's where we miss having unification as a primitive...
def rule_id_to_canonical(RuleId, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.rule_for_matching:
        Table = lgm_tables.rule_for_matching[Key0]
    else:
        return 'no_canonical_found'
    [Rule] = Table[tuple([RuleId])]
    CanonicalWords = Rule["*-->"][0]["*:"][1][0]["*/"][1]
    return " ".join(CanonicalWords)

# ======================================================================

# DP PARSING

def tf_idf_parse_rule(RuleId, WordsAndContext0, Namespace, Domain):
    WordsAndContext = add_dicts_to_words_and_content(WordsAndContext0)
    init_tf_idf_parse_rule(RuleId, WordsAndContext, Namespace, Domain)
    (HeadSem, Body) = head_sem_and_body_for_rule_id(RuleId, Namespace, Domain)
    Results = tf_idf_parse_rule_body(Body, WordsAndContext, Namespace, Domain)
    Results1 = add_tiebreaking_parallelism_factor_to_results(Results, WordsAndContext)
    SortedResults = sorted(Results1, key=lambda x: x[2], reverse=True)
    (MatchedSentence, MatchedSem, Score, Trace) = SortedResults[0]
    Sem0 = substitute_rhs_sem(HeadSem, MatchedSem)
    Sem = reduce_sem(Sem0)
    SimplifiedTrace = simplify_trace(Trace)
    return ( MatchedSentence, Sem, Score, SimplifiedTrace )

# When we have multiple results with the same score, we want to prefer the more parallel one
def add_tiebreaking_parallelism_factor_to_results(Results, WordsAndContent):
    return [ add_tiebreaking_parallelism_factor_to_result(Result, WordsAndContent) for Result in Results ]

def add_tiebreaking_parallelism_factor_to_result(Result, WordsAndContext):
    Words = WordsAndContext[0]
    ( Matched, Sem, Score, Trace ) = Result 
    Weight = -0.0000001
    TiebreakingParallelismFactor = Weight * w.WagnerFischer(Matched, Words).cost
    return ( Matched, Sem, Score + TiebreakingParallelismFactor, Trace )

def add_dicts_to_words_and_content(WordsAndContext):
    ( Words, Context ) = WordsAndContext
    return ( Words, Context, words_to_dict(Words), words_to_dict(Context) )

def head_sem_and_body_for_rule_id(RuleId, Namespace, Domain):
    Rule = get_rule_for_rule_id(RuleId, Namespace, Domain)
    ( Head, Body ) = Rule["*-->"]
    HeadSem = Head["*:"][1][0]
    return [ HeadSem, Body ]
    
def get_rule_for_rule_id(RuleId, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.rule_for_matching:
        Table = lgm_tables.rule_for_matching[Key0]
    else:
        return []
    Key = tuple([RuleId])
    if Key in Table :
        return Table[Key][0]
    else:
        return []

# This global dictionary is where we keep the best matches for each non-terminal/phrase relevant to the current match
tf_idf_parse_for_phrase_rule = {}

# Populate tf_idf_parse_for_phrase_rule, moving bottom-up
def init_tf_idf_parse_rule(RuleId, WordsAndContext, Namespace, Domain):
    global tf_idf_parse_for_phrase_rule
    tf_idf_parse_for_phrase_rule = {}
    PhraseRules = get_phrase_rules_for_rule(RuleId, Namespace, Domain)
    store_tf_idf_parses_for_phrase_rules(PhraseRules, WordsAndContext, Namespace, Domain)

#phrase_rules_for_rule = {
#    tuple(["babeldr__abdominal__27-avez-vous mal au ventre ?"]):[[ "babeldr__abdominal__mal_au_ventre", "babeldr__abdominal__avez_vous" ]]
#}

def get_phrase_rules_for_rule(RuleId, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.phrase_rules_for_rule:
        Table = lgm_tables.phrase_rules_for_rule[Key0]
    else:
        return []
    Key = tuple([RuleId])
    if Key in Table:
        return Table[Key][0]
    else:
        return []

# The phrase rules should be ordered by depth, so those called by the higher ones
# will be stored by the time they are needed.

def store_tf_idf_parses_for_phrase_rules(PhraseRules, WordsAndContext, Namespace, Domain):
    for PhraseRuleId in PhraseRules:
        store_tf_idf_parses_for_phrase_rule(PhraseRuleId, WordsAndContext, Namespace, Domain)

# Find the best match for each phrase rule and store it in tf_idf_parse_for_phrase_rule, indexed by PhraseRuleId
def store_tf_idf_parses_for_phrase_rule(PhraseRuleId, WordsAndContext, Namespace, Domain):
    global tf_idf_parse_for_phrase_rule
    if not at_least_one_phrase_rule_for_matching(PhraseRuleId, Namespace, Domain):
        print('*** Error: unable to find phrase rules for ' + PhraseRuleId)
    else:
        tf_idf_parse_for_phrase_rule[PhraseRuleId] = do_tf_idf_parse_for_phrase_rule(PhraseRuleId, WordsAndContext, Namespace, Domain)

def at_least_one_phrase_rule_for_matching(PhraseRuleId, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.phrase_rule_for_matching :
        Table = lgm_tables.phrase_rule_for_matching[Key0]
    else:
        return False
    Key = tuple([PhraseRuleId, 1])
    return Key in Table

# To match a phrase rule, match the input using each associated definition and then pick the ones with the best score
def do_tf_idf_parse_for_phrase_rule(PhraseRuleId, WordsAndContext, Namespace, Domain):
    Rules = get_all_phrase_rules_for_phrase_rule_id(PhraseRuleId, Namespace, Domain)
    Results = concat_lists([ do_tf_idf_parse_for_single_phrase_rule(Rule, WordsAndContext, Namespace, Domain) for Rule in Rules ])
    SortedResults = sorted(Results, key=lambda x: x[2], reverse=True)
    return SortedResults[:parameters.n_dp_candidates]

# Unpack the phrase rule, parse using the body, then substitute the sem values
def do_tf_idf_parse_for_single_phrase_rule(Rule, WordsAndContext, Namespace, Domain):
    ( Head, Body ) = Rule["*-->"]
    ( HeadCat, HeadSem ) = Head["*:"]
    Results = tf_idf_parse_rule_body(Body, WordsAndContext, Namespace, Domain)
    return [ substitute_sem_in_phrase_result(Result, HeadCat, HeadSem) for Result in Results ]

def substitute_sem_in_phrase_result(Result, HeadCat, HeadSem):
    ( MatchedSentence, MatchedSem, Score, Trace ) = Result
    Sem = substitute_rhs_sem(HeadSem, MatchedSem)
    return ( MatchedSentence, { HeadCat:Sem }, Score, Trace )

def get_all_phrase_rules_for_phrase_rule_id(PhraseRuleId, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.phrase_rule_for_matching:
        Table = lgm_tables.phrase_rule_for_matching[Key0]
        return get_all_phrase_rules_for_phrase_rule_id1(PhraseRuleId, 1, [], Table)
    else:
        format('*** Error: no phrase rules loaded for namespace "{0}" and domain "{1}"'.format(Namespace, Domain)),
        return []
    
def get_all_phrase_rules_for_phrase_rule_id1(PhraseRuleId, I, ListSoFar, Table):
    Key = tuple([PhraseRuleId, I])
    if not Key in Table:
        return ListSoFar
    else:
        NewRule = Table[Key][0]
        return get_all_phrase_rules_for_phrase_rule_id1(PhraseRuleId, I + 1, ListSoFar + [ NewRule ], Table)

# The main DP matching function: separate into different cases depending on what kind of constituent it is.
# (These are the choices in (b)-(e) of step 4 of §5 in the SLSP 2017 paper)
def tf_idf_parse_rule_body(Body, WordsAndContext, Namespace, Domain):
    global tf_idf_parse_for_phrase_rule
    #print('Parse body: ' + str(Body) )
    if Body == []:
        return tf_idf_parse_rule_body_null(WordsAndContext, Namespace, Domain)
    elif body_is_single_word(Body):
        Word = body_to_single_word(Body)
        return tf_idf_parse_rule_body_word(Word, WordsAndContext, Namespace, Domain)
    elif body_is_sequence(Body):
        [ P, Q ] = body_to_sequence_components(Body)
        return tf_idf_parse_rule_body_sequence([ P, Q ], WordsAndContext, Namespace, Domain)
    elif body_is_alternation(Body):
        List = body_to_alternation_list(Body)
        return tf_idf_parse_rule_body_alternation(List, WordsAndContext, Namespace, Domain)
    elif body_is_phrase_rule_id(Body):
        PhraseRuleId = body_to_phrase_rule_id(Body)
        return tf_idf_parse_for_phrase_rule[PhraseRuleId]
    else:
        print('*** Error: Unable to parse body: ' + str(Body))
        return False

# [ "est-ce" ]
def body_is_single_word(Body):
    return isinstance(Body, list) and len(Body) == 1

def body_to_single_word(Body):
    return Body[0]

# { "*,":[ [ "fait" ], [ "mal" ] ] }
def body_is_sequence(Body):
    return isinstance(Body, dict) and "*," in Body

def body_to_sequence_components(Body):
    return Body["*,"]

# { "*or":[ [ { "*,":[ [ "est-ce" ], [ "que" ] ] }, [] ] ] }
def body_is_alternation(Body):
    return isinstance(Body, dict) and "*or" in Body

def body_to_alternation_list(Body):
    return Body["*or"][0]

# "babeldr__abdominal__avez_vous"
def body_is_phrase_rule_id(Body):
    return isinstance(Body, str)

def body_to_phrase_rule_id(Body):
    return Body

# Null. Return null values.
def tf_idf_parse_rule_body_null(WordsAndContext, Namespace, Domain):
    Result = [ [], {}, 0.0, [] ]
    return [ Result ]

# Single word. Use the tf-idf score if it's there, otherwise apply the no-match penalty.
def tf_idf_parse_rule_body_word(Word, WordsAndContext, Namespace, Domain):
    ( Words, Context, WordsDict, ContextDict ) = WordsAndContext
    if Word in Words:
        Score = idf_score_for_word(Word, Namespace, Domain)
        Trace = [[Word, 'w', Score]]
    elif Word in Context:
        Score = parameters.context_weight * idf_score_for_word(Word, Namespace, Domain)
        Trace = [[Word, 'c', Score]]
    else:
        Score = parameters.no_match_penalty
        Trace = [[Word, 'skipped', Score]]
    Result = [ [Word], {}, Score, Trace ]
    return [ Result ]

# Sequence. Match each part separately, then add the scores and combine the semantics.
def tf_idf_parse_rule_body_sequence(Body, WordsAndContext, Namespace, Domain):
    [ P, Q ] = Body
    ResultsP = tf_idf_parse_rule_body(P, WordsAndContext, Namespace, Domain)
    ResultsQ = tf_idf_parse_rule_body(Q, WordsAndContext, Namespace, Domain)
    AllResults = [ combine_sequence_results(ResultP, ResultQ, WordsAndContext) for ResultP in ResultsP for ResultQ in ResultsQ ]
    return sorted(AllResults, key=lambda x: x[2], reverse=True)[:parameters.n_dp_candidates]

def combine_sequence_results(ResultP, ResultQ, WordsAndContext):
    [ MatchedWords1, Sem1, Score1, Trace1 ] = ResultP
    [ MatchedWords2, Sem2, Score2, Trace2 ] = ResultQ
    Sem1Copy = dict.copy(Sem1)
    Sem1Copy.update(Sem2)  # i.e. update Sem1Copy with values from Sem2, changing Sem1
    MatchedWords = MatchedWords1 + MatchedWords2
    Trace = combine_traces(Trace1, Trace2, WordsAndContext)
    return [ MatchedWords, Sem1Copy, trace_to_score(Trace), Trace ]

# When we combine the elements of a sequence, we may find that we've overused the words
# from the input. If so, correct by turning matches into skips.
def combine_traces(Trace1, Trace2, WordsAndContext):
    ( Words, Context, WordsDict, ContextDict ) = WordsAndContext
    Trace = []
    CurrentWordsDict = {}
    CurrentContextDict = {}
    for TraceElement in Trace1 + Trace2:
        ( Word, Type, Score ) = TraceElement
        if Type == 'w':
            inc_dict(CurrentWordsDict, Word)
            if CurrentWordsDict[Word] > WordsDict[Word]:
                TraceElement1 = [ Word, 'skipped', parameters.no_match_penalty ]
            else:
                TraceElement1 = TraceElement
        elif Type == 'c':
            inc_dict(CurrentContextDict, Word)
            if CurrentContextDict[Word] > ContextDict[Word]:
                TraceElement1 = [ Word, 'skipped', parameters.no_match_penalty ]
            else:
                TraceElement1 = TraceElement
        else:
            TraceElement1 = TraceElement
        Trace = Trace + [ TraceElement1 ]
    return Trace

def trace_to_score(Trace):
    return sum([ TraceElement[2] for TraceElement in Trace ])
    
# Alternation. Match each part separately, concatenate, keep the ones with the highest scores.
def tf_idf_parse_rule_body_alternation(List, WordsAndContext, Namespace, Domain):
    AllResults = concat_lists([ tf_idf_parse_rule_body(Body, WordsAndContext, Namespace, Domain) for Body in List ])
    return sorted(AllResults, key=lambda x: x[2], reverse=True)[:parameters.n_dp_candidates]

##======================================================================

# SUBSTITUTING SEM VALUES FROM NON-TERMINALS

# [ { "*/":[ "unit", [ "avez-vous", "mal", "au", "ventre", "?" ] ] } ]

def substitute_rhs_sem(Sem, MatchedSem):
    if Sem == []:
        return {}
    elif isinstance(Sem, (list, tuple)) and len(Sem) == 1 and isinstance(Sem[0], dict):
        TagSemIn = Sem[0]
        [Tag, SemIn] = TagSemIn["*/"]
        return substitute_rhs_sem1(SemIn, MatchedSem)
    elif isinstance(Sem, dict):
        TagSemIn = Sem
        [Tag, SemIn] = TagSemIn["*/"]
        return substitute_rhs_sem1(SemIn, MatchedSem)
    else:
        print('Error: unknown first arg to substitute_rhs_sem: ' + str(Sem))
        return None

def substitute_rhs_sem1(Sem, MatchedSem):
    if Sem == []:
        return []
    elif isinstance(Sem, str):
        return [Sem]
    elif isinstance(Sem, (tuple, list)):
        F = Sem[0]
        R = Sem[1:]
        return substitute_rhs_sem_item(F, MatchedSem) + substitute_rhs_sem1(R, MatchedSem)

def substitute_rhs_sem_item(Item, MatchedSem):
    if isinstance(Item, str):
        return [ Item ]
    elif is_tr_phrase(Item):
        PhraseId = tr_phrase_to_phrase_id(Item)
        if PhraseId in MatchedSem:
            return MatchedSem[PhraseId]
        else:
            print('Error: no value for "' + str(PhraseId) + '" in ' + str(MatchedSem))

def is_tr_phrase(Item):
    return isinstance(Item, dict) and '*tr_phrase' in Item

def tr_phrase_to_phrase_id(Item):
    return Item['*tr_phrase'][0]

def reduce_sem(WordList):
    Atom0 = " ".join(WordList)
    return remove_nospace_markers_in_atom(Atom0)

def remove_nospace_markers_in_atom(Atom):
    return Atom.replace(" *nospace* ", "")
	
# ======================================================================

# RESORTING THE DP-PARSED RESULTS

def sort_match_results_by_score(Results, Namespace, Domain, WordsAndContextAtoms):
    if parameters.rescoring_strategy == 'none':
        return Results
    elif parameters.rescoring_strategy == 'tf_idf_penalizing_unmatched':
        ResultsNext = [ add_tf_idf_penalizing_unmatched_scores_to_result(Result, Namespace, Domain, WordsAndContextAtoms) for Result in Results ]
        return sorted(ResultsNext, key=lambda x: x['tf_idf_penalizing_unmatched'], reverse=True)
        
def add_tf_idf_penalizing_unmatched_scores_to_result(Result, Namespace, Domain, WordsAndContextAtoms):
    BasicTdfIdfScore = Result['score']
    ( WordsAtom, ContextAtom ) = WordsAndContextAtoms
    #WordsAtom = WordsAndContextAtoms[0].lower()
    MatchedAtom = Result['matched']
    Unmatched = unmatched_words_in_word_atom(WordsAtom, MatchedAtom)
    ContextFactor = context_parallelism_factor(MatchedAtom, ContextAtom)
    Score = BasicTdfIdfScore + len(Unmatched) * parameters.no_match_penalty + ContextFactor
    Result.update({'tf_idf_penalizing_unmatched':Score})
    return add_unmatched_words_and_context_factor_to_trace(Result, Unmatched, ContextFactor)

def unmatched_words_in_word_atom(WordsAtom, MatchedAtom):
    return [ UnmatchedWord for UnmatchedWord in WordsAtom.split() if not UnmatchedWord in MatchedAtom.split() ]

def add_unmatched_words_and_context_factor_to_trace(Result, Unmatched, ContextFactor):
    OldTrace = Result['trace']
    NewTrace = OldTrace + [ [ Word, 'skipped' ] for Word in Unmatched ] + [ [ 'context_bonus', ContextFactor] ]
    Result.update({'trace':NewTrace})
    return Result

def context_parallelism_factor(MatchedAtom, ContextAtom):
    Weight = parameters.context_parallelism_bonus
    if ( Weight != 0 and ContextAtom != '' ):
        return Weight * w.WagnerFischer(MatchedAtom, ContextAtom).cost
    else:
        return 0.0

# ======================================================================

# GETTING TF-IDF SCORES

def idf_score_for_word(Word, Namespace, Domain):
    strategy = parameters.idf_score_strategy
    if strategy == 'simple':
        return simple_idf_score_for_word(Word, Namespace, Domain)
    elif Strategy == 'logarithmic':
        return logarithmic_idf_score_for_word(Word, Namespace, Domain)

def simple_idf_score_for_word(Word, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.rules_for_word:
        Table = lgm_tables.rules_for_word[Key0]
    else:
        return 0.0
    [Freq, RuleIds] = Table[tuple([Word, Namespace, Domain])]
    if Freq > 0:
        return 1.0 / Freq
    else:
        return 0.0

def combine_tf_and_idf_scores(TfScore, IdfScore):
    return IdfScore
	
def add_bonus_for_low_scoring_rule(RuleId, Namespace, Domain, Score):
    N = parameters.prioritise_low_scoring_rules
    if N > 0 and get_minimum_score_rank_for_rule(RuleId, Namespace, Domain) <= N:
        return Score + 1
    else:
        return Score

def get_minimum_score_rank_for_rule(RuleId, Namespace, Domain):
    Key0 = tuple([Namespace])
    if Key0 in lgm_tables.minimum_score_for_rule:
        Table = lgm_tables.minimum_score_for_rule[Key0]
    else:
        return 1000
    Key = tuple([RuleId, Namespace, Domain])
    if Key in Table:
        return Table[Key][1]
    else:
        return 1000

# ======================================================================

def simplify_trace(Trace):
    return [ simplify_trace_element(Element) for Element in Trace ]

def simplify_trace_element(Element):
    ( Word, Type, Score ) = Element
    if Type == 'skipped':
        return [ Word, 'skipped' ]
    elif Type == 'w':
        return [ Word, Score ]
    else:
        return [ mark_word_as_from_context(Word), Score ]

def mark_word_as_from_context(Word):
    return '(' + Word + ')'

# ======================================================================

# UTILITIES

def words_to_dict(Words):
    Dict = {}
    for Word in Words:
        inc_dict(Dict, Word)
    return Dict

def inc_dict(Dict, Word):
    if Word in Dict:
        Dict[Word] = Dict[Word] + 1
    else:
        Dict[Word] = 1

def concat_lists(ListOfLists):
    return [ Item for List in ListOfLists for Item in List ]
