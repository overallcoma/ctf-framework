import argparse
from pydub import AudioSegment

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
args = parser.parse_args()
flag = args.flag

if args.flag is None:
    print("Please specify a flag with -f")
    exit(1)
else:
    flag = args.flag
    flag = flag.upper()

outputfilename = "./output.wav"
output_data = AudioSegment.empty()


def add_letter_to_output(letter):
    if letter == " ":
        silentaudio = AudioSegment.silent(duration=750)
        return silentaudio
    target_audio_file = ('./sounds/' + letter + '.mp3')
    target_audio_file = AudioSegment.from_file(target_audio_file, format="mp3")
    target_audio_file += AudioSegment.silent(duration=350)
    return target_audio_file


for char in flag:
    output_data += add_letter_to_output(char)

output_data.export(outputfilename, format="wav")
