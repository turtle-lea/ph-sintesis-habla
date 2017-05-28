#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

os.system("rm -rf generated")
os.system("mkdir generated")

# OSx (MAC) no permite guardar un mismo archivo de forma case sensitive
# Por ejemplo: ka.wav y kA.wav. Por eso se utiliza 'ax' como
# representación de la A mayúscula.
os.system("praat diphone_generation.praat ka")
os.system("praat diphone_generation.praat kax")
os.system("praat diphone_generation.praat la")
os.system("praat diphone_generation.praat lax")
os.system("praat diphone_generation.praat ma")
os.system("praat diphone_generation.praat max")
os.system("praat diphone_generation.praat pa")
os.system("praat diphone_generation.praat pax")
os.system("praat diphone_generation.praat sa")
os.system("praat diphone_generation.praat sax")
os.system("praat diphone_generation.praat ax")

param = sys.argv[1]
is_question = False
if "?" in param:
	is_question = True
param = param.translate(None, "?")
output_file = sys.argv[2]
entry = "_" + param + "_"
praat_file = "praat_generated.praat"
generated_audio_file = output_file
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

# Una tupla (time, pitch_value) es un punto a partir del cual debe modificarse
# la prosodia cuando en los 8 puntos siguientes el pitch_sigue siendo continuo
# (no hay rupturas o quiebres en el pitch) y al mismo tiempo, se advierte
# un aumento brusco del pitch respecto al valor del pitch anterior (>= 9 Hz)
def matching_point(i, arr):
	return continuous_pitch(i, arr) and prosodia_increment(i, arr)

def continuous_pitch(i, arr):
	res = (i + 7 < len(arr)) and all(arr[j+1][0] - arr[j][0] <= 0.04 for j in range(i, i+7))
	return res

def prosodia_increment(i, arr):
	return i != 0 and (arr[i][1] - arr[i-1][1] >= 9)

diphones = diphones(entry)
diphones_index = {}

for index, item in enumerate(entry[0:len(entry)-1]):
	value = entry[index] + entry[index+1]
	value = value.replace("A", "ax")
	diphones_index[index] = value

keys = diphones_index.keys()

# INICIO Generación dinámica del script praat para concatenación de difonos
# Se guarda con el nombre "praat_generated.praat"
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

os.system("praat " + praat_file + " " + param)
# FIN Generación dinámica del script praat para concatenación de difonos


# En el caso de que la entrada contenga un signo de interrogación se realiza este paso adicional
if is_question:
	extraer_pitch_script = "extraer-pitch-track.praat"
	pitch_tier_file = "generated_audio.PitchTier"
	pitch_tier_file_modified = "generated_audio_modified.PitchTier"

	os.system("praat " + extraer_pitch_script + " " + generated_audio_file + " " + pitch_tier_file + " " + "50 300")
	value_filter_characters = "value ="
	number_filter_characters = "number ="

	pitch_values = []
	time_values = []

	# Lectura de los valores del PitchTier (pitch and time)
	with open(pitch_tier_file, 'r') as f:
		for line in f:
			if 'number' in line:
				value = line.translate(None, number_filter_characters)
				time_values.append(float(value))
			if 'value' in line:
				value = line.translate(None, value_filter_characters)
				pitch_values.append(float(value))

	number_of_points = len(time_values)
	time_and_pitch = [[time_values[i], pitch_values[i]] for i in range(number_of_points)]

	question_secuence = [185.0, 195.0, 204.0, 209.0, 208.0, 201.0, 192.0, 180.0]

	# Obtención de los puntos en donde debe modificarse la prosodia para que suene como pregunta
	# Ver función matching_point
	# Se busca los índices a partir de los cuales debe iniciarse una modificación de prosodia,
	# y se reemplaza los 8 valores subsiguientes con la secuencia que contiene la prosodia
	# de una pregunta: 'question_secuence'
	indexes = [i for i, x in enumerate(time_and_pitch) if matching_point(i, time_and_pitch)]
	values = [x[1] for x in time_and_pitch]

	# Reemplazo de los valores del pitch en los puntos de modificación con la secuencia de valores
	# propios de las preguntas
	for i in indexes:
		values[i: i+8] = question_secuence

	# Escritura del nuevo PitchTier modificado. 'generated_audio_modified.PitchTier'
	with open(pitch_tier_file_modified, 'w') as f_modified:
		with open(pitch_tier_file, 'r+b') as f_read:
			i = 0
			for line in f_read:
				if 'value' in line:
					f_modified.write("\t" + "value = " + str(values[i]) + "\n")
					i += 1
				else:
					f_modified.write(line)

	# Reemplazo del audio file con el nuevo file en forma de pregunta
	os.system("praat reemplazar-pitch-track.praat " + generated_audio_file + " " + "generated_audio_modified.PitchTier " + generated_audio_file + " 50 300")

print "Audio successfully generated"
