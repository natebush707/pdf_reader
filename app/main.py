import pyttsx3
import PyPDF2
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
# C:\Users\17072\Desktop\pdf_reader\CSUSB_Student_Handbook.pdf

# set up cli argument parser
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
optional = parser._action_groups.pop()
required = parser.add_argument_group('required arguments')
required.add_argument("-p", "--path", type=str, required=True, help="Absolute path to target .pdf file.")
optional.add_argument("-b", "--begin", default=0, type=int, help="Beginning page.")
optional.add_argument("-e", "--end", default=0, type=int, help="Ending page.")
optional.add_argument("-v", "--volume", default=200, type=int, help="Volume.")
optional.add_argument("-m", "--mode", default=0, type=int, help="Voice mode selection {0:male robot, 1:female robot}.")
optional.add_argument("-s", "--speed", default=200, type=int, help="Voice reading speed.")
optional.add_argument("-r", "--read", action="store_true", default=True, help="Narrate the file immediately.")
optional.add_argument("-nr", "--no-read", dest="read", action="store_false", help="Disable immediate narration.")

parser._action_groups.append(optional)
args = vars(parser.parse_args())

# input validation for beginning and ending pages
if args.get('begin') > args.get('end'):
    print('Invalid beginning and ending page numbers provided.')
    raise SystemExit(1)

# parse .pdf name and build audio filename
pdf_name = args.get('path').split('\\')[-1][0:-4]
audio_filename = f'{pdf_name}_pg{args.get("begin")}_to_pg{args.get("end")}.mp3'

# load .pdf 
pdf = open(args.get('path'), 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf, strict = False)

# check document length against requested ending page
num_pages = pdf_reader.getNumPages()
if args.get('end') > num_pages:
    print(f'Provided ending page is invalid. Document only has {num_pages} pages.')
    raise SystemExit(1)

# initiliaze voice engine and settings
voice_engine = pyttsx3.init()
voice_engine.setProperty('rate', args.get('speed'))
voice_engine.setProperty('volume', args.get('volume'))
voice_selection = voice_engine.getProperty('voices')
voice_engine.setProperty('voice', voice_selection[args.get('mode')].id)

# extract requested pages from .pdf
extracted_text = ""
for i in range(args.get('begin'), args.get('end') + 1):
    text = pdf_reader.getPage(i)
    extracted_text += text.extractText()

# output voice and .mp3 file
if args.get('read'):
    voice_engine.say(extracted_text)
voice_engine.save_to_file(extracted_text, audio_filename)
voice_engine.runAndWait()
voice_engine.stop()