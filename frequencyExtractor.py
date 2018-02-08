import re
import sys

if len(sys.argv) < 3 :
  print("Usage: python frequencyExtrator.py input.log output.tsv")

input = sys.argv[1]
output = sys.argv[2]

FREQUENCY_START = "Harmonic frequencies"
rotational = ""
translational = ""
frequencies = []

def handleLineInFreqChunk(line) :
  if line.strip().startswith("Frequencies") :
    arr = re.split(" +", line.strip())
    for i in range(2, len(arr)) :
      frequencies.append(arr[i])

def extractTranslational(line) :
  if line.startswith(" Translational  ") :
    arr = re.split(" +", line.strip())
    return arr[3]

def extractRotational(line) :
  if line.startswith(" Rotational  ") :
    arr = re.split(" +", line.strip())
    return arr[3]

with open(input, "r") as fin :
  freq = False
  for line in fin :
    if len(line.strip()) == 0 :
      continue
    if line.startswith(" Vibration ") :
      break

    if freq :
      if line.strip().startswith("-") :
        freq = False
      else :
        handleLineInFreqChunk(line)
    else :
      if line.strip().startswith(FREQUENCY_START) :
        freq = True
      else :
        val = extractRotational(line)
        if val :
          rotational = val
        val = extractTranslational(line)
        if val :
          translational = val

with open(output, "w") as fout :
  fout.write("mode\tv (cm-1)\n")
  mode = 1
  for item in frequencies :
    fout.write(str(mode) + "\t" + item + "\n")
    mode += 1

  fout.write("\n")
  fout.write("rotational\t" + rotational + "\n")
  fout.write("transl.\t" + translational)  