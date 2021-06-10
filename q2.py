import argparse
import logging
import os
import hashlib


def md5_file(file_a_lines, file_b_lines):
    diffs = {}
    md5_a = hashlib.md5()
    md5_b = hashlib.md5()
    for index, line in enumerate(file_a_lines):
        md5_a.update(bytes(str(line).strip(), 'utf-8'))
        md5_a = md5_a.hexdigest()

        md5_b.update(bytes(str(file_b_lines[index]).strip(), 'utf-8'))
        md5_b = md5_b.hexdigest()

        if md5_a != md5_b:
            if md5_a in diffs.keys() and md5_b in diffs.keys():
                diffs[md5_a] += 1
                diffs[md5_b] += 1
            if md5_a in diffs.keys() and md5_b not in diffs.keys():
                diffs[md5_a] += 1
                diffs[md5_b] = 1
            if md5_a not in diffs.keys() and md5_b in diffs.keys():
                diffs[md5_b] += 1
                diffs[md5_a] = 1
            if md5_a not in diffs.keys() and md5_b not in diffs.keys():
                diffs[md5_a] = 1
                diffs[md5_b] = 1

        md5_a = hashlib.md5()
        md5_b = hashlib.md5()
    return diffs


def find_files_to_cmp(folder_a, folder_b):
    file_to_cmp = []
    for root, dirs, files in os.walk(folder_a):
        for file in files:
            if os.path.isfile(os.path.join(folder_b, file)):
                file_to_cmp.append((
                    os.path.join(folder_a, file),
                    os.path.join(folder_b, file)
                ))
    return file_to_cmp


def cmp_files(folder_a, folder_b, verbose=False):
    logger = logging.getLogger('CMP')
    formter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
    log_file = logging.FileHandler('logger.log')
    log_file.setFormatter(formter)
    logger.addHandler(log_file)

    logger.setLevel(logging.DEBUG)
    if verbose:
        logger.setLevel(logging.INFO)
        logging.basicConfig(level=logging.INFO)

    cmp_list = find_files_to_cmp(folder_a, folder_b)
    status = False
    for file in cmp_list:
        f1 = open(file[0])
        f2 = open(file[1])

        f1_lines = f1.readlines()
        f2_lines = f2.readlines()

        f1.close()
        f2.close()

        if len(f1_lines) != len(f2_lines):
            logger.info(f'The {file} files are not in same length - they are not the same')
            continue
        else:
            not_diffs = []
            file_diffs = md5_file(f1_lines, f2_lines)
            for key in file_diffs:
                if file_diffs[key] % 2 == 0:
                    not_diffs.append(key)
            for k in not_diffs:
                file_diffs.pop(k)
            if file_diffs:
                status = True
                logger.info(f'The {file} files are not identical')
            else:
                logger.info(f'The {file} files are identical')

    if status:
        logger.info(f'Failed')
    return status


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', action='store', dest='folder_a', type=str, help='folder a to compare')
    parser.add_argument('-b', action='store', dest='folder_b', type=str, help='folder b to compare')
    parser.add_argument('-v', dest='verbose', action='store_true', default=False, help='verbose')
    args = parser.parse_args()

    # folder_a = r'C:\Users\shlomog\Desktop\Shay\folder_A'
    # folder_b = r'C:\Users\shlomog\Desktop\Shay\folder_B'
    if cmp_files(args.folder_a, args.folder_b, args.verbose):
        print('Failed')
		exit(500)
