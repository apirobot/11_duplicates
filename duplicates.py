import argparse
import os.path
from os import walk
from collections import defaultdict


def is_dir(path):
    """Checks if ``path`` is an actual directory."""
    if not os.path.isdir(path):
        msg = '{0} is not a directory'.format(path)
        raise argparse.ArgumentTypeError(msg)
    else:
        return path


def create_parser():
    parser = argparse.ArgumentParser(description='Anti-Duplicator')
    parser.add_argument('directory', metavar='DIR', type=is_dir,
                        help='path to a directory')
    return parser


def get_duplicates(directory):
    fname_and_fsize_to_fpathes = defaultdict(list)
    for (dirpath, dirnames, filenames) in walk(directory):
        for filename in filenames:
            fpath = os.path.abspath(os.path.join(dirpath, filename))
            if os.path.isfile(fpath):
                fsize = os.path.getsize(fpath)
                fname_and_fsize_to_fpathes[filename+str(fsize)].append(fpath)

    duplicates = [fpathes for fpathes in fname_and_fsize_to_fpathes.values()
                          if len(fpathes) > 1]
    return duplicates


def main():
    parser = create_parser()
    args = parser.parse_args()

    duplicates = get_duplicates(args.directory)

    for i, fpathes in enumerate(duplicates):
        print('{:5} | '.format(i+1))
        for fpath in fpathes:
            print('{:5} | {}'.format('', fpath))
        print('\n')


if __name__ == '__main__':
    main()
