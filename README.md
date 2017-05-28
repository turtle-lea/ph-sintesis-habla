TP1 sintesis del habla
Grupo: Leandro Matayoshi (únicamente). LU=79/11

El backend-tts se corre utilizando el comando:
python tts.py mamAsalAlapApa? output.wav
según lo indicado por el enunciado

Para funcionar, genera automáticamente los difonos en la carpeta 'generated/', utilizando el script 'diphone_generation.praat',
que al mismo tiempo utiliza el script proporcionado por la cátedra: 'save_labeled_intervals_to_wav_sound_files.praat'

Luego utiliza la entrada para generar dinámicamente el script: 'praat_generated.praat', que generará la concatenación de difonos.

En el caso de que la entrada sea una pregunta, se agrega un paso adicional en donde:
1) Se utiliza "extraer-pitch-track.praat", obteniendo un archivo "generated_audio.PitchTier"
2) Se modifica ese archivo, generando uno nuevo: "generated_audio.PitchTier"
3) Se utiliza el script reemplazar-pitch-track.praat


Heurística utilizada para la modificación de la prosodia en el caso de las preguntas:

En un principio se utilizó la opción 'Manipulate' de Praat para experimentar y
determinar qué características particulares se observanen el caso de las preguntas.
Con esta aproximación, se observó que un aspecto determinante está constituído por una elevación
del valor del pitch en las 'Aes' acentuadas de la palabra. Esto sucede de forma natural: En 'mamAma', el valor del pitch
cuando se pronuncia la A es mayor que en los demás difonos. Sin embargo, en el caso de las preguntas, los valores del pitch
se acentúan todavía más.

En el caso de mi voz, el pitch en los difonos: mA y Am en el caso de una afirmación ronda el valor de los 135 Hz, mientras
que en una pregunta alcanza los 209 Hz.

Para que suene más natural, luego de observar los PitchTiers resultantes de la modificación manual, se observó que este valor
de 209 Hz no se alcanza de forma abrupta, sino en forma de una curva suave (similar a una cuadrática que alcanza su valor)
máximo.

De esta manera, se obtuvo empíricamente una secuencia de 8 valores (en Hz):
[185.0, 195.0, 204.0, 209.0, 208.0, 201.0, 192.0, 180.0], que aplicados a lo largo de 1 décima de segundo
replican la prosodia de una pregunta para los difonos acentuados en el caso del hablante "Leandro Matayoshi".

Por lo tanto, la heurística consiste en encontrar los puntos del pitch en donde la prosodia es mayor (debido a que
coinciden con las A mayúsculas), y acentuarlas todavía más reemplazando sus valores por los de la secuencia.
