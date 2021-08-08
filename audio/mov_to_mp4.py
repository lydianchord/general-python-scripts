import argparse
import subprocess


def make_mp4(mov_files):
    for mov_file in mov_files:
        stem = mov_file.rsplit('.', 1)[0]
        subprocess.call([
            'ffmpeg', '-y', '-i', '{}.mov'.format(stem), '-c', 'copy',
            '-movflags', '+faststart', '{}.mp4'.format(stem)
        ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mov', nargs='*')
    args = parser.parse_args()
    
    if args.mov:
        make_mp4(args.mov)
    else:
        parser.print_help()
