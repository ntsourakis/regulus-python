#!/usr/bin/python

# Abstract strings to German strings

def german_strings():
    return {# Normal responses
            'yes': '<audio src="SYSTEM_AUDIO_DIR/success.mp3"/>',
            'yes {string}': '{string} <audio src="SYSTEM_AUDIO_DIR/success.mp3"/> ',
            'no {string}': 'Ich hörte {string} <audio src="SYSTEM_AUDIO_DIR/failure.mp3"/>',
            'no {string} {prompt}': 'Ich hörte {string} <audio src="SYSTEM_AUDIO_DIR/failure.mp3"/> {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Next: {prompt}': 'Weiter: {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            '{prompt}': '{prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Exit': 'Spiel wird beendet. Danke und auf Wiederhören',
            'Repeat. {text}': 'Wiederholen. {text}',
            'Back: {prompt}': 'Zurück: {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Waiting. {prompt}': 'Ich warte. {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Help: the answer is {text}. {prompt}': 'Hilfe: die Antwort ist {text} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Help: the answer is {text}. {prompt} (then continue)': 'Hilfe: die Antwort ist {text} <break time="0.5s"/> ',
            'Lessons: {lessons}': 'Lektionen: {lessons} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Lesson: {lesson}. {prompt}': 'Lektion: {lesson}. {prompt} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            # Conjunctions
            '{t1}, {t2}': '{t1}, {t2}',
            '{t1} or {t2}': '{t1} oder {t2}',
            # Errors
            'Unknown lesson': 'Unbekannte Lektion <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'At end of lesson {score} {max_possible_score}':
               'Die Lektion ist beendet. Ergebnis: {score} von {max_possible_score} <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'At beginning of lesson': 'Das ist der Beginn der Lektion <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'No help is available': 'Entschuldigung, keine Hilfe ist verfügbar <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Nothing to repeat': 'Es gibt nichts zu wiederholen <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'I don\'t understand': 'Ich habe es nicht verstanden. Können Sie das bitte wiederholen? <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>',
            'Something went wrong': 'Etwas ist schief gelaufen <audio src="SYSTEM_AUDIO_DIR/end_of_turn.mp3"/>'
            }
