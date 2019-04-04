##discard_out_of_domain(yes).
##%discard_out_of_domain(no).

discard_out_of_domain = 'yes'

##word_regularisation_strategy(remove_casing).
##%word_regularisation_strategy(remove_punctuation).
##%word_regularisation_strategy(shorten_to_n_chars(6)).
##word_regularisation_strategy(guess_words(0.67)).

word_regularisation_strategy = {'remove_casing':'yes',
                                'remove_punctuation':'yes',
                                'remove_hyphens_and_apostrophes':'yes',
                                'guess_words': 0.8}

oov_shortlist_length = 50

##idf_score_strategy(simple).
##%idf_score_strategy(logarithmic).

idf_score_strategy = 'simple'

##tf_score_strategy(none).
##%tf_score_strategy(multiplicative).

tf_score_strategy = 'none'

##no_match_penalty(Penalty) :-
##	(   no_match_penalty_disabled ->
##	    Penalty = 0.0
##	;
##	    otherwise ->
##	    no_match_penalty0(Penalty)
##	).
##
##% For "simple"
##%no_match_penalty0(-0.09).
##%no_match_penalty0(-0.14).
##no_match_penalty0(-0.18).
##%no_match_penalty0(-0.24).

no_match_penalty = -0.18

context_weight = 0.2

context_parallelism_bonus = -0.02

##% For "logarithmic"
##%no_match_penalty(-1.98).
##%no_match_penalty(-2.16).
##%no_match_penalty(-2.4).
##
##%prioritise_low_scoring_rules(0).
##%prioritise_low_scoring_rules(1).
##prioritise_low_scoring_rules(3).
##%prioritise_low_scoring_rules(5).

prioritise_low_scoring_rules = 3

##%use_minimal_length_strings(yes).
##use_minimal_length_strings(no).

use_minimal_length_strings = 'no'

##%rescoring_strategy(tf_idf).
##rescoring_strategy(tf_idf_penalizing_unmatched).
##%rescoring_strategy(word_error).
##%rescoring_strategy(tf_idf_weighted_word_error).
##%rescoring_strategy(char_error).
##%rescoring_strategy(common_ngrams).
##%rescoring_strategy(none).

#rescoring_strategy = 'none'
rescoring_strategy = 'tf_idf_penalizing_unmatched'

n_dp_candidates = 2

##%glm_confidence_threshold(0.50).
##%glm_confidence_threshold(0.55).
##%glm_confidence_threshold(0.60).
##glm_confidence_threshold(0.65).
##%glm_confidence_threshold(0.70).

glm_confidence_threshold = 0.65
