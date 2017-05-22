form Generated
	sentence name
endform

prefix$ = "sources/" + name$
Read from file: prefix$ + ".wav"
Read from file: prefix$ + ".TextGrid"

selectObject: "Sound " + name$
plusObject: "TextGrid " + name$

runScript: "save_labeled_intervals_to_wav_sound_files.praat", 1, 1, 0, "yes", "yes", "yes", 0.01, "generated/" + name$ + "/", "", ""





