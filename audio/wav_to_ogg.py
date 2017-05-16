import argparse
import os
import subprocess
import sys


def find_folder():
    folders = [x for x in os.listdir() if '_ogg' in x and os.path.isdir(x)]
    if len(folders) == 0:
        sys.exit('Please create a folder containing "_ogg" in its name')
    else:
        folder = folders[0]
        print('Found folder: {}\n'.format(folder))
    return folder


def wav_to_ogg(folder, filenames):
    for filename in filenames:
        file_base = filename.split('.', 1)[0]
        print(file_base)
        subprocess.call([
            'sox', file_base + '.wav', '-C', '9',
            '{}/{}.ogg'.format(folder, file_base)
        ])


def convert_all(folder):
    wav_to_ogg(folder, (x for x in os.listdir() if x.endswith('.wav')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='*')
    parser.add_argument('-A', '--all', action='store_true')
    args = parser.parse_args()
    folder = find_folder()
    if args.all is True:
        convert_all(folder)
    elif len(args.filename):
        wav_to_ogg(folder, args.filename)
    else:
        parser.print_help()
