import abjad
from random import randrange
import tk
import os
import mido
import rtmidi
import note_notations as nn
current_directory = os.getcwd()

random_number = randrange(12)
print('Random note to listen to:',random_number, nn.human_readable_notes[random_number])

# abjad is a python library for creating music notation
# set the duration of the note to 1/4
duration = abjad.Duration(1, 4)
# abjad uses 0 for C, 1 for C#, 2 for D and so on so we subtract 4 to get the correct note
abjad_random_number = (random_number - 4) % 12
# if the random number is even we add 12 to get the next octave which is 50% chance
if randrange(2) == 0:
    abjad_random_number += 12
# create a note with the random number and the duration
notes = [abjad.Note(abjad_random_number, duration)]
staff = abjad.Staff(notes)

# print the staff to a file
print(abjad.persist.as_png(staff, current_directory+'/output/test'))
# print(abjad.persist.as_ly(staff, current_directory+'/output/neww'))
# print(abjad.persist.as_midi(staff, current_directory+'/output/neww'))
# print(abjad.persist.as_pdf(staff, current_directory+'/output/neww'))

print('Current backend:', mido.backend)

outports = mido.get_output_names()
inports = mido.get_input_names()
print('Available outports:', outports)
print('Available inports:', inports)


# doing this i can send midi messages to for example garageband
if outports:
    outport_name = next((name for name in outports if 'roland' in name.lower()), None)
    if outport_name:
        with mido.open_output(outport_name) as outport:
            msg = mido.Message('note_on', note=20+36+ random_number, velocity=35)
            outport.send(msg)
    else:
        print('No Roland MIDI outport available')
        exit()
else:
    print('No MIDI outports available')
    exit()

# If there are any input ports available
if inports:
    inport_name = next((name for name in inports if 'roland' in name.lower()), None)
    if inport_name:
        with mido.open_input(inport_name) as inport:
            print('Listening to:', inport.name)
            # Continuously listen to the input port
            print(nn.human_readable_notes)
            while True:
                # Wait for a message and print it
                try:
                    msg = inport.receive()
                    if msg.type == 'note_on' and msg.velocity > 0:
                        # first A of the piano starts with 21 hence we subtract 20
                        note_received = (msg.note - 20) % 12
                        if note_received in nn.human_readable_notes and note_received == random_number:
                            print('Correct note:', nn.human_readable_notes[note_received])
                            break
                        else:
                            print('Wrong note:', nn.human_readable_notes[note_received])

                except KeyboardInterrupt:
                    break
    else:
        print('No Roland MIDI inport available')
        exit()
else:
    print('No MIDI inports available')	
    exit()
