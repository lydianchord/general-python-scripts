import argparse
import os
import subprocess


def find_folder():
    folders = [x for x in os.listdir() if '_ogg' in x and os.path.isdir(x)]
    if len(folders) == 1:
        folder = '%s/' % folders[0]
        print('Found folder: %s' % folders[0])
    else:
        folder = ''
        print('Did not find folder containing "_ogg" in name')
    print()
    return folder


def wav_to_ogg(filename, folder=''):
    file_base = filename.split('.', 1)[0]
    print(file_base)
    subprocess.call(['sox', '%s.wav' % file_base, '-C', '9', '%s%s.ogg' % (folder, file_base)])


def convert_all(folder=''):
    wav_files = [x for x in os.listdir() if x.endswith('.wav')]
    for f in wav_files:
        wav_to_ogg(f, folder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?')
    parser.add_argument('-A', '--all', action='store_true')
    args = parser.parse_args()
    folder = find_folder()
    if args.all is True:
        convert_all(folder)
    elif args.filename is not None:
        wav_to_ogg(args.filename, folder)
    else:
        parser.print_help()
