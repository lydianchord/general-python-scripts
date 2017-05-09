import os
import subprocess
import sys


def find_folder_and_image():
    folders = [x for x in os.listdir() if '_avi' in x and os.path.isdir(x)]
    if len(folders) == 1:
        folder = '%s/' % folders[0]
        print('Found folder: %s\n' % folders[0])
    else:
        sys.exit('Did not find folder containing "_avi" in name')
    try:
        image = [x for x in os.listdir(folder) if x.endswith('.png')][0]
    except IndexError:
        sys.exit('Did not find image')
    return folder, image


def make_avi(folder, png_file, wav_file):
    subprocess.call([
        'ffmpeg', '-y', '-loop', '1', '-i', folder + png_file, '-i', wav_file,
        '-c:a', 'copy', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17',
        '-shortest', folder + wav_file.replace('.wav', '.avi')
    ])


def convert_all(folder, png_file):
    wav_files = [x for x in os.listdir() if x.endswith('.wav')]
    for wav_file in wav_files:
        make_avi(folder, png_file, wav_file)


if __name__ == '__main__':
    convert_all(*find_folder_and_image())
