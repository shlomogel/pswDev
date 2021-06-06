import os
import shutil
import logging
import stat
import subprocess
import argparse


class Git:
    def __init__(self, directory, git, verbose=False):
        self.clone_cmd = f"git clone {git}"
        self.git_name = str(git).split('/')[-1]
        self.clone_base_directory = directory
        self.clone_directory = os.path.join(self.clone_base_directory, self.git_name)
        if verbose:
            self.logger = logging.getLogger('GIT')
            self.formter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
            self.log_file = logging.FileHandler('logger.log')
            self.log_file.setFormatter(self.formter)
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(self.log_file)
            logging.basicConfig(level=logging.INFO)

    def chmod_dir(self):
        for root, dirs, files in os.walk(self.clone_directory):
            # print(dirs)
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)

    def create_dir(self):
        if os.path.exists(self.clone_base_directory):
            self.logger.info(f'Folder {self.clone_base_directory} already exists')
            # check if this dir is git repo.
            # if its not git directory create new folder inside
            os.chdir(self.clone_directory)
            if '.git' in os.listdir(self.clone_directory):
                self.logger.info(f'{self.clone_directory} is git folder')
                # chmod directory
                self.chmod_dir()
                # delete directory
                os.chdir(self.clone_base_directory)
                shutil.rmtree(self.clone_directory)
                self.logger.info(f'Folder {self.clone_directory} was removed')
            else:
                self.logger.info(f'The directory is not git folder, Continue... ')
        else:
            self.logger.info(f'Folder {self.clone_base_directory} doesnt exists, Creating...')
            os.makedirs(self.clone_base_directory)

    def check_git(self):
        if '.git' in os.listdir(self.clone_directory):
            self.logger.info(f'{self.clone_directory} is git folder')
            return True
        return False

    def os_clone(self):
        clone = True
        # create clone dir:
        self.create_dir()
        # change to clone folder
        os.chdir(self.clone_base_directory)
        self.logger.info(f'Changing to {self.clone_base_directory}')
        # run git clone command
        # os.system(self.clone_cmd)
        p = subprocess.Popen(self.clone_cmd.split(), stderr=subprocess.PIPE)
        for line in p.stderr:
            if 'fatal' in str(line):
                clone = False
            self.logger.info(f'{str(line)}')
        # see if the .git folder exists
        if clone:
            clone = self.check_git()
            if clone:
                self.logger.info(f'git clone {self.git_name} finished successfully')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--git', action='store', dest='git', type=str, help='git repo')
    parser.add_argument('-d', '--dir', action='store', dest='dir_path', type=str, help='clone to')
    parser.add_argument('-v', dest='verbose', action='store_true', default=False, help='verbose')
    args = parser.parse_args()

    git = Git(args.dir_path, args.git, args.verbose)
    git.os_clone()

#
# d = r'C:\Users\shlomog\Desktop\1'
# g = r'https://github.com/shlomogel/pswDev'
#
