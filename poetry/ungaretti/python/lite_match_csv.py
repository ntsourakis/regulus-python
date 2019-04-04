
# ---------------------------------------------------

import ungaretti.python.lite_grammar_match
import csv 
import time
import sys

# ---------------------------------------------------

def test_matching_on_csv(spreadsheet_in, namespace, domain, n, spreadsheet_out):
    print("Reading and processing spreadsheet: " + spreadsheet_in)
    read_and_process_spreadsheet(spreadsheet_in, namespace, domain, n, spreadsheet_out)
    print("\nWritten spreadsheet: " + spreadsheet_out)

def test_babeldr_20170101():
    test_matching_on_csv('C:/cygwin64/home/speech/medslt-code/trunk/MedSLT2/Fre/corpora/PythonMatcherFrenchTest.csv',
                         'babeldr', 'abdominal', 13,
                         'C:/cygwin64/home/speech/medslt-code/trunk/MedSLT2/Fre/corpora/PythonMatcherFrenchTestResults.csv')

def test_small():
    test_matching_on_csv('C:/cygwin64/home/speech/medslt-code/trunk/MedSLT2/Fre/corpora/PythonMatcherFrenchTestSmall.csv',
                         'babeldr', 'abdominal', 13,
                         'C:/cygwin64/home/speech/medslt-code/trunk/MedSLT2/Fre/corpora/PythonMatcherFrenchTestSmallResults.csv')

# ---------------------------------------------------

# Open the input and output files and process each row, skipping the header
def read_and_process_spreadsheet(spreadsheet_in, namespace, domain, n, spreadsheet_out):
    out_fieldnames = ['Transcription', 'Recognised', 'Canonical', 'TranscriptionResult', 'RecResult', 'TTime', 'RTime']
    scores = init_scores()
    with open(spreadsheet_in, 'r', encoding="utf-8") as csv_infile:
        reader = csv.reader(csv_infile, delimiter='\t', quotechar='"')
        with open(spreadsheet_out, 'w') as csv_outfile:
            writer = csv.DictWriter(csv_outfile, fieldnames=out_fieldnames, delimiter='\t', quotechar='"')
            writer.writeheader()
            i = 1
            for row in reader:
                # Skip header row
                if ( not is_header_row(row) ):
                    i = process_spreadsheet_row(row, namespace, domain, n, writer, scores, i)
    print_scores(scores)

def init_scores():
    return {'TranscriptionCorrect': 0, 'RecCorrect': 0, 'Processed': 0, 'TranscriptionTime':0.0, 'RecTime':0.0}

def is_header_row(row):
    return ( row[0] == 'Transcription' )

def process_spreadsheet_row(row, namespace, domain, n, writer, scores, i):
    transcription = row[0]
    recognised = row[1]
    canonical = row[2]

    # Skip examples with no canonical 
    if canonical != 'null':
        ( trans_results, trans_time ) = timed_match_string(transcription, namespace, domain, n)
        ( rec_results, rec_time) = timed_match_string(recognised, namespace, domain, n)
    
        ( trans_n, rec_n ) = score_results(canonical, trans_results, rec_results, trans_time, rec_time, scores)

        writer.writerow({'Transcription': transcription, 
                         'Recognised': recognised, 
                         'Canonical': canonical,
                         'TranscriptionResult': trans_n,
                         'RecResult': rec_n, 
                         'TTime': three_digits(trans_time), 
                         'RTime': three_digits(rec_time)})
        print_a_dot(i)
        return i + 1
    else:
        return i

def timed_match_string(string, namespace, domain, n):
    start = time.time()
    results = lite_grammar_match.match_string(string, n, namespace, domain)
    end = time.time()
    diff = end - start
    return ( results, diff )

def score_results(canonical, trans_results, rec_results, trans_time, rec_time, scores):
    trans_n = position_of_canonical_in_results(canonical, trans_results)
    rec_n = position_of_canonical_in_results(canonical, rec_results)
    
    scores['Processed'] = scores['Processed'] + 1
    if trans_n == 1:
        scores['TranscriptionCorrect'] = scores['TranscriptionCorrect'] + 1
    if rec_n == 1:
        scores['RecCorrect'] = scores['RecCorrect'] + 1
    scores['TranscriptionTime'] = scores['TranscriptionTime'] + trans_time
    scores['RecTime'] = scores['RecTime'] + rec_time
    
    return ( trans_n, rec_n )

def position_of_canonical_in_results(canonical, results):
    return position_of_canonical_in_results1(canonical, results, 1)

def position_of_canonical_in_results1(canonical, results, I):
    if results == []:
        return 'not_found'
    elif results[0]['canonical'] == canonical:
        return I
    else:
        return position_of_canonical_in_results1(canonical, results[1:], I + 1)

def print_scores(scores):
    processed = scores['Processed']
    trans_correct = scores['TranscriptionCorrect']
    rec_correct = scores['RecCorrect']
    trans_time = scores['TranscriptionTime']
    rec_time = scores['RecTime']
   
    if processed > 0 :
        trans_error_rate = 1 - trans_correct / processed
        rec_error_rate = 1 - rec_correct / processed
        av_trans_time = trans_time / processed
        av_rec_time = rec_time / processed
    else:
        trans_error_rate = 'undefined'
        rec_error_rate = 'undefined'
        av_trans_time = 'undefined'
        av_rec_time = 'undefined'

    print('\n')
    print('Error rate (transcriptions) ' + three_digits(trans_error_rate) )
    print('Error rate (rec results)    ' + three_digits(rec_error_rate) )
    print('Av. time  (transcriptions)  ' + three_digits(av_trans_time) )
    print('Av. time  (rec results)     ' + three_digits(av_rec_time) )
    print('Processed                   ' + str(processed) )

def three_digits(x):
    if x == 'undefined':
        return 'undefined'
    else:
        return ( "%.3f" % x )

def print_a_dot(i):
    sys.stdout.write('.')
    if i%100 == 0:
        sys.stdout.write(' (' + str(i) + ')\n')
    sys.stdout.flush()
    
