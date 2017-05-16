import argparse
import os
import subprocess
import sys


def find_folder_and_image():
    try:
        folder = [x for x in os.listdir() if '_avi' in x and os.path.isdir(x)][0]
        print('Found folder: {}'.format(folder))
    except IndexError:
        sys.exit('Please create a folder containing "_avi" in its name')
    
    try:
        image = [x for x in os.listdir(folder) if x.endswith('.png')][0]
        print('Found image: {}\n'.format(image))
    except IndexError:
        sys.exit('Please add a PNG image to the output folder')
    
    return folder, image


def make_avi(folder, png_file, wav_files):
    for wav_file in wav_files:
        subprocess.call([
            'ffmpeg', '-y', '-loop', '1', '-i',
            '{}/{}'.format(folder, png_file), '-i', wav_file, '-c:a', 'copy',
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-shortest',
            '{}/{}'.format(folder, wav_file.replace('.wav', '.avi'))
        ])


def convert_all(folder, png_file):
    make_avi(folder, png_file, (x for x in os.listdir() if x.endswith('.wav')))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('wavfile', nargs='*')
    parser.add_argument('-A', '--all', action='store_true')
    args = parser.parse_args()
    folder, image = find_folder_and_image()
    if args.all is True:
        convert_all(folder, image)
    elif args.wavfile:
        make_avi(folder, image, args.wavfile)
    else:
        parser.print_help()
