#!/usr/bin/python

# Abstract strings to English strings

def english_strings():
    return {# Normal responses
            'yes': '<audio src="SYSTEM_AUDIO_DIR/success.mp3"/>',
            'yes {string}': '{string} <audio src="SYSTEM_AUDIO_DIR/success.mp3"/> ',
            'no {string}': 'I heard {string}. <audio src="SYSTEM_AUDIO_DIR/failure.mp3"/>',
            'no {string} {prompt}': 'I heard {string}. <audio src="SYSTEM_AUDIO_DIR/failure.mp3"/> {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Next: {prompt}': 'Next: {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            '{prompt}': '{prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Exit': 'Exit. Thank you and goodbye.',
            'Repeat. {text}': 'Repeat. {text}',
            'Back: {prompt}': 'Back: {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Waiting. {prompt}': 'Waiting. {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Help: the answer is {text}. {prompt}': 'Help: the answer is {text} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Help: the answer is {text}. {prompt} (then continue)': 'Help: the answer is {text} <break time="0.5s"/> ',
            'Lessons: {lessons}': 'Lessons: {lessons} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Lesson: {lesson}. {prompt}': 'Lesson: {lesson}. {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            # Conjunctions
            '{t1}, {t2}': '{t1}, {t2}',
            '{t1} or {t2}': '{t1} or {t2}',
            # Errors
            'Unknown lesson': 'Unknown lesson <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'At end of lesson {score} {max_possible_score}':
               'End of lesson. Score: {score} out of {max_possible_score} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'At beginning of lesson': 'At beginning of lesson <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'No help is available': 'Sorry, no help is available <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Nothing to repeat': 'There is nothing to repeat <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'I don\'t understand': 'I\'m sorry, don\'t understand. Could you please repeat? <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Something went wrong': 'Something went wrong <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>'
            }
