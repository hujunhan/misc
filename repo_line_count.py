## A script to count the number of lines of code in a directory of git repositories

import glob
import pathlib
repo_path='/Users/hu/code/lidar/oh_my_loam'

## Get the list of all the souce file in the repo

source_extentions=['.py','.cpp','.h','.c','.hpp','.m','.mm','.java']

file_list=glob.glob(repo_path+'/**/*',recursive=True)
total_line_count=0
for file in file_list:
    file_path=pathlib.Path(file)
    if file_path.is_file() and file_path.suffix in source_extentions:
        with open(file,'r') as f:
            data=f.read()
            total_line_count+=len(data.split('\n'))

print(total_line_count)