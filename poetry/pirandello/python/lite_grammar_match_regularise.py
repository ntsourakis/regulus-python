#!/usr/bin/python

import pirandello.python.lite_grammar_match_tables as lgm_tables
import pirandello.python.lite_grammar_match_parameters as parameters
import pirandello.python.wagnerfischer as w
import math

# ======================================================================

# REGULARISING INPUT

def convert_input_and_context_to_words_list(InputStringAndContext, Namespace, Domain):
    (Input, Context) = InputStringAndContext
    return ( convert_atom_to_words_list(Input, Namespace, Domain),
             # The context will already be regularised, so we don't need to do that again
             convert_atom_to_words_list_minimal(Context, Namespace, Domain) )

def convert_words_list_to_words_atom(WordsListAndContext):
    (Input, Context) = WordsListAndContext
    return ( " ".join(Input),
             " ".join(Context) )

def convert_atom_to_words_list_minimal(String, Namespace, Domain):
    Strategy = parameters.word_regularisation_strategy
    #return String.split()
    return split_string_into_words(String, Strategy)

def regularise_string(String, Namespace, Domain):
    RegularisedWordList = convert_atom_to_words_list(String, Namespace, Domain)
    return " ".join(RegularisedWordList)

def convert_atom_to_words_list(String, Namespace, Domain):
    Strategy = parameters.word_regularisation_strategy
    #Words = String.split()
    Words = split_string_into_words(String, Strategy)
    return [ regularise_word(Word, Strategy, Namespace, Domain) for Word in Words ]

def regularise_word(Word, Strategy, Namespace, Domain):
    Word1 = maybe_lowercase(Word, Strategy)
    Word2 = maybe_remove_punctuation(Word1, Strategy)
    Word3 = maybe_guess_word(Word2, Strategy, Namespace, Domain)
    return Word3

def maybe_lowercase(Word, Strategy):
    if ( 'remove_casing' in Strategy and Strategy['remove_casing'] == 'yes' ):
         return Word.lower()
    else:
         return Word

def maybe_remove_punctuation(Word, Strategy):
    if ( 'remove_punctuation' in Strategy and Strategy['remove_punctuation'] == 'yes' ):
        return remove_punctuation(Word)
    else:
        return Word

def maybe_guess_word(Word, Strategy, Namespace, Domain):
    if 'guess_words' in Strategy:
        init_domain_vocabulary_if_necessary(Namespace, Domain)
        return guess_word(Word, Strategy['guess_words'], Namespace, Domain)
    else:
        return Word

# ======================================================================

def split_string_into_words(String, Strategy):
    if 'remove_hyphens_and_apostrophes' in Strategy and Strategy['remove_hyphens_and_apostrophes'] == 'yes':
        # Replace hyphens with spaces and add spaces after apostrophes
        String1 = String.replace('-', ' ').replace('\'', '\' ')
    else:
        String1 = String
    return String1.split()

def remove_punctuation(String):
    return ''.join(ch for ch in String if ch not in "!?,():;")
  
# ======================================================================

domain_vocabulary = {}
guessed_oov_words = {}
all_words_and_vectors = {}
oov_initialised = False

def init_domain_vocabulary_if_necessary(Namespace, Domain):
    Key0 = tuple([Namespace, Domain])
    if not Key0 in domain_vocabulary:
        init_domain_vocabulary(Namespace, Domain)

def init_domain_vocabulary(Namespace, Domain):
    global domain_vocabulary
    global guessed_oov_words
    global oov_initialised
    Key0Tables = tuple([Namespace])
    Key0 = tuple([Namespace, Domain])
    guessed_oov_words[Key0] = {}
    domain_vocabulary[Key0] = {}
    if Key0Tables in lgm_tables.rules_for_word:
        Table = lgm_tables.rules_for_word[Key0Tables]
        for Key in Table:
            Word = Key[0]
            domain_vocabulary[Key0][Key] = word_to_vector(Word)
        init_all_words_and_vectors_table(Namespace, Domain)
        oov_initialised = True
        print('--- Initialised OOV word guessing for namespace = "{0}" and domain = "{1}"'.format(Namespace, Domain))
    else:
        print('*** Warning: unable to find rules_for_word table for namespace "{}", could not initialise OOV word guessing.'.format(Namespace))

def init_all_words_and_vectors_table(Namespace, Domain):
    global all_words_and_vectors
    Key0 = tuple([Namespace, Domain])
    all_words_and_vectors[Key0] = find_all_words_and_vectors(Namespace, Domain)
        
def find_all_words_and_vectors(Namespace, Domain):
    global domain_vocabulary
    Key0 = tuple([Namespace, Domain])
    return [ (Key[0], domain_vocabulary[Key0][Key] ) for Key in domain_vocabulary[Key0] ]

def get_all_words_and_vectors(Namespace, Domain):
    global all_words_and_vectors
    Key0 = tuple([Namespace, Domain])
    if Key0 in all_words_and_vectors :
        return all_words_and_vectors[Key0]
    else:
        return []

def guess_word(Word, Threshold, Namespace, Domain):
    global domain_vocabulary
    global oov_initialised
    Key0 = tuple([Namespace, Domain])
    if not oov_initialised:
        return Word
    elif not Key0 in domain_vocabulary:
        return Word
    elif ( Word == '' ):
        return Word
    elif in_vocabulary(Word, Namespace, Domain):
        return Word
    elif guessed_oov_word(Word, Namespace, Domain):
        return guessed_oov_word(Word, Namespace, Domain)
    else:
        ( GuessedWord, Score ) = guess_oov_word(Word, Namespace, Domain)
        if ( Score >= Threshold ):
            store_guessed_oov_word(Word, Namespace, Domain, GuessedWord)
            return GuessedWord
        else:
            return Word

def in_vocabulary(Word, Namespace, Domain):
    global domain_vocabulary
    return tuple([Word, Namespace, Domain]) in domain_vocabulary

def guessed_oov_word(Word, Namespace, Domain):
    global guessed_oov_words
    Key0 = tuple([Namespace, Domain])
    Key = tuple([Word])
    if Key0 in guessed_oov_words and Key in guessed_oov_words[Key0] :
        return guessed_oov_words[Key0][Key]
    else:
        return False

def store_guessed_oov_word(Word, Namespace, Domain, GuessedWord):
    global guessed_oov_words
    Key0 = tuple([Namespace, Domain])
    Key = tuple([Word])
    guessed_oov_words[Key0][Key] = GuessedWord

def guess_oov_word(Word, Namespace, Domain):
    AllWordsAndVectors = get_all_words_and_vectors(Namespace, Domain)
    Shortlist = get_oov_shortlist(Word, AllWordsAndVectors)
    return guess_oov_word1(Word, Shortlist)

def get_oov_shortlist(Word, AllWordsAndVectors):
    N = parameters.oov_shortlist_length
    Vector = word_to_vector(Word)
    ScoredWords = [ [ Word1, inner_product(Vector, Vector1) ]
                    for (Word1, Vector1) in AllWordsAndVectors ]
    SortedScoredWords = sorted(ScoredWords, key=lambda x: x[1], reverse=True)
    return SortedScoredWords[:N]

def guess_oov_word1(Word, Shortlist):
    ScoredWords = [ [ Word1, string_match_score(Word, Word1) ] for
                    ( Word1, CosineScore ) in Shortlist ]
    SortedScoredWords = sorted(ScoredWords, key=lambda x: x[1], reverse=True)
    return SortedScoredWords[0]

def string_match_score(Word, Word1):
    Length = len(Word)
    if ( Length == 0 ):
        return 0
    else:
        return ( Length - w.WagnerFischer(Word, Word1).cost ) / Length

# -----------------------------------------

# Representing words as sparse vectors so we can do cosine distance efficiently

def word_to_vector(Word):
    return normalise_vector(list_to_vector(word_features(Word), {}))

def word_features(Word):
    return list(Word) + char_bigrams(Word)

def list_to_vector(List, Vec):
    if ( List == [] ):
        return Vec
    else:
        inc_count(Vec, List[0])
        return list_to_vector(List[1:], Vec)

def inc_count(Vec, Key):
    if ( Key in Vec ):
        Vec[Key] = Vec[Key] + 1
    else:
        Vec[Key] = 1

def normalise_vector(Vec):
    VecLength = vector_length(Vec)
    if ( VecLength == 0 ):
        VecLengthInverse = 1
    else:
        VecLengthInverse = 1.0 / VecLength
    return scalar_multiply(VecLengthInverse, Vec)

def vector_length(Vec):
    return math.sqrt(sum([ Vec[Key] * Vec[Key] for Key in Vec ]))

def scalar_multiply(K, Vec):
    return { Key:( K * Vec[Key]) for Key in Vec }

def inner_product(Vec1, Vec2):
    return sum([ Vec1[Key] * Vec2[Key] for Key in Vec1 if Key in Vec2 ] )

def char_bigrams(Word):
    if ( len(Word) < 2 ):
        return []
    else:
        return [ tuple([ Word[I], Word[I+1] ]) for I in range(0, len(Word)-1) ]
    


    
        
        
