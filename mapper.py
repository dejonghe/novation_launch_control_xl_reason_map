#! /usr/bin/env python3

import argparse

# This is what the lua script needs to map midi to a name of an input
# {pattern="B0 0D xx", name="User 1 Track 1 Knob 1", port=1},

# There are 16 midi templates, 8 User, 8 Factory
# user starts at B0 176 ends at B7 183
# factory starts at B8 184 ends at BF 191

# There are 3 rows of knobs, the midi hex increases by left to right on each row
# knobRow1 starts at 0D 13 ends at 14 20 
# knobRow2 starts at 1D 29 ends at 24 36
# knobRow3 starts at 31 49 ends at 38 56
# faders follow the same pattern
# fader1 starts at 4D 77 ends at 54 84

# Buttons are a bit different, still need to map these
# button1 part1 starts at 29 ends at 2C
# button1 part2 starts at 39 end at 3C
# button2 part1 starts at 49 end at 4C
# button2 part2 starts at 59 end at 5C

def midi_mapping():
    bank_count = 1
    for bank in range(176,192):
        bank_name = "User" if bank <= 183 else "Factory"
        track_count = 1
        row_count = 1 
        row_value = 13
        knob_rows = [ 13,29,49 ]
        fader_rows = [ 77 ] 
        for row_start in knob_rows + fader_rows:
            thing_count = 0
            thing_name = 'Knob' if row_start in knob_rows else 'Fader'
            while thing_count < 8:
                knob_value = row_start + thing_count 
                #print(f"                {{pattern=\"{hex(bank).lstrip('0x').zfill(2).upper()} {hex(knob_value).lstrip('0x').zfill(2).upper()} xx\", name=\"{bank_name} {bank_count} Track {thing_count + 1} {thing_name} {row_count if thing_name == 'Knob' else '1'}\"}},")
                print(f"                {{name=\"{bank_name} {bank_count} Track {thing_count + 1} {thing_name} {row_count if thing_name == 'Knob' else '1'}\", input=\"value\", output=\"value\", min=0, max=127}},")
                thing_count = thing_count + 1 
            row_count = row_count + 1
        bank_count = bank_count + 1 if bank_count < 8 else 1


# Mappings 
# Map     User 1 Track 2 Fader 1          Channel 1 Level
def remote_mapping():
    channel = 1
    bank_count = 1
    for bank in range(1,17):
        for track in range(1,9):
            bank_name = 'User' if bank <= 8 else 'Factory'
            print(f"Map\t{bank_name} {bank_count} Track {track} Fader 1\t\tChannel {channel} Level")
            channel = channel + 1
        bank_count = bank_count + 1 if bank_count < 8 else 1



def main():
    parser = argparse.ArgumentParser(description='map midi stuff for novation')
    parser.add_argument('-r','--remote-map', help='print the remote map', action='store_true', dest='remote_map')
    parser.add_argument('-m','--midi-map', help='print the midi map', action='store_true', dest='midi_map')
    args = parser.parse_args()

    if args.remote_map:
        remote_mapping()
    elif args.midi_map:
        midi_mapping()

if __name__ == '__main__':
    try: main()
    except: raise
