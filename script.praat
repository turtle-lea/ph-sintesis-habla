Read from file: "la/l.wav"
Read from file: "la/la.wav"
Read from file: "la/al.wav"

select Sound l
Copy: "l2"
select Sound la
Copy: "la2"
select Sound al
Copy: "al2"

select Sound l
Copy: "l3"
select Sound la
Copy: "la3"
select Sound al
Copy: "al3"

select Sound l
Copy: "l4"
select Sound la
Copy: "la4"
select Sound al
Copy: "al4"

select Sound l
plus Sound la
plus Sound al
plus Sound la2
plus Sound al2
plus Sound la3
plus Sound al3
plus Sound la4
plus Sound al4

Concatenate recoverably
selectObject: "Sound chain"
Write to WAV file... motivation2.wav
