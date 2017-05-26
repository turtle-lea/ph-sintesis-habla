#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.system("rm -rf generated")
os.system("mkdir generated")

os.system("praat script.praat ka")
os.system("praat script.praat kax")
os.system("praat script.praat la")
os.system("praat script.praat lax")
os.system("praat script.praat ma")
os.system("praat script.praat max")
os.system("praat script.praat pa")
os.system("praat script.praat pax")
os.system("praat script.praat sa")
os.system("praat script.praat sax")
os.system("praat script.praat ax")

param = sys.argv[1]
entry = "_" + param + "_"
praat_file = "praat_generated.praat"
generated_audio_file = "generated_audio.wav"
generated_textgrid_file = "generated_audio.TextGrid"

def diphones(entry):
	res = []
	for index, item in enumerate(entry[0:len(entry)-1]):
		res.append(entry[index] + entry[index+1])
	return  res

def read_ff(d):
	return "Read from file: \"generated/" + d + ".wav\""

def select_sound(d):
	return "select Sound " + str(d)

def plus_sound(d):
	return "plus Sound " + str(d)

def concatenate_recoverably():
	return "Concatenate recoverably\n"

def select_chain():
	return "selectObject: \"Sound chain\" \n"

def select_chain_textgrid():
	return "selectObject: \"TextGrid chain\" \n"

def write_to_wav_file(filename):
	return "Write to WAV file... " + filename + "\n"

def write_to_text_grid_file(filename):
	return "Save as text file: \"" + filename + "\"" + "\n"

def rename(index):
	return "Rename: " + "\"" + str(index) + "\""

diphones = diphones(entry)
diphones_index = {}

for index, item in enumerate(entry[0:len(entry)-1]):
	value = entry[index] + entry[index+1]
	value = value.replace("A", "ax")
	diphones_index[index] = value

keys = diphones_index.keys()

with open(praat_file, 'w') as f:
	for k in keys:
		f.write(read_ff(diphones_index[k]))
		f.write('\n')
		f.write(rename(k))
		f.write('\n')	

	f.write(select_sound(keys[0]))
	f.write('\n')

	for k in keys[1:]:
		f.write(plus_sound(k))
		f.write('\n')	

	f.write(concatenate_recoverably())

	f.write(select_chain())
	f.write(write_to_wav_file(generated_audio_file))
	f.write(select_chain_textgrid())
	f.write(write_to_text_grid_file(generated_textgrid_file))

extraer_pitch_script = "extraer-pitch-track.praat"
pitch_tier_file = "generated_audio.PitchTier"

os.system("praat " + praat_file + " " + param)
os.system("praat " + extraer_pitch_script + " " + generated_audio_file + " " + pitch_tier_file + " " + "50 300")
filter_characters = "value ="

values = []
with open(pitch_tier_file, 'r') as f:
	for line in f:
		if 'value' in line:
			value = line.translate(None, filter_characters)
			values.append(float(value))

print values
print len(values)


print diphones
print "Done"
