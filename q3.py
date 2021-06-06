import argparse
import logging
import os
from py7zr import py7zr
from q1 import Git
from q2 import cmp_files


def main_pipline(git, clone, verbose=False):
    pipline_status = 0
    # 1. git pull
    try:
        git = Git(clone, git, verbose)
        git.os_clone()
    except Exception:
        raise Exception

    # 2. extract 7z files
    try:
        logger = logging.getLogger('ZIP')
        formter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
        log_file = logging.FileHandler('logger.log')
        log_file.setFormatter(formter)
        logger.addHandler(log_file)

        logger.setLevel(logging.DEBUG)
        if verbose:
            logger.setLevel(logging.INFO)
            logging.basicConfig(level=logging.INFO)

        git_dir = git.clone_directory
        folders = []

        for file in os.listdir(git_dir):
            if file.endswith('.7z'):
                extract_dir = git_dir
                with py7zr.SevenZipFile(os.path.join(git_dir, file), 'r') as archive:
                    archive.extractall(path=extract_dir)
                logger.info(f'{file} extract successfully')
                folders.append(os.path.join(git_dir, str(file).split('.')[0]))
    except Exception:
        raise Exception

    # 3. compare files
    try:
        if cmp_files(folder_a=folders[0], folder_b=folders[1], verbose=verbose):
            pipline_status = 500
    except Exception:
        raise Exception
    # 4. status
    return pipline_status


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--git', action='store', dest='git', type=str, help='git repo')
    parser.add_argument('-d', '--dir', action='store', dest='dir_path', type=str, help='clone to')
    parser.add_argument('-v', dest='verbose', action='store_true', default=False, help='verbose')
    args = parser.parse_args()

    exit(main_pipline(args.git, args.dir_path, args.verbose))
