import pathlib
from json import dumps, load

this_repo = 'https://github.com/frate-templates/index.git'

class Branch:
    def __init__(self, name, hash):
        self.name = name
        self.hash = hash

def get_branches(git_url):
    import subprocess

    branches = []
    try:
        ls_remote_str = subprocess.check_output(['git', 'ls-remote', '--heads', git_url]).decode('utf-8').split()
        for i in range(0, len(ls_remote_str), 2):
            branches.append(Branch(ls_remote_str[i+1].split('/')[2], ls_remote_str[i]))
        return branches
    except subprocess.CalledProcessError:
        return None

def get_head_hash(git_url):
    import subprocess
    try:
        return subprocess.check_output(['git', 'ls-remote', git_url, 'HEAD']).decode('utf-8').split()[0]
    except subprocess.CalledProcessError:
        return None

def get_latest_hash(git_url):
    import subprocess
    try:
        return subprocess.check_output(['git', 'ls-remote', git_url, 'HEAD']).decode('utf-8').split()[0]
    except subprocess.CalledProcessError:
        return None


sources = []
for dir in pathlib.Path('../srcs').iterdir():
    if dir.is_dir():
        file = pathlib.Path(dir)/'index.json'
        if not (file.exists()):
            print(f"Error: {file} does not exist")
            continue
        with open(file, 'r') as f:
            data = load(f)
            if not data.get('git') or not data.get('description'):
                print(f"Error: {file} has missing data")
                continue
            data['name'] = dir.name
            data['head'] = get_head_hash(data['git'])
            data['branches'] = []
            try:
                branches = get_branches(data['git'])
                data['branches'] = {}
                if branches is None:
                    print(f"Error: {file} failed to get branches repo may not exist or it may be private")
                    continue
                for branch in branches:
                    data['branches'][branch.name] = branch.hash;
            except Exception as e:
                print(e.__class__.__name__)
                print(f"Error: {file} failed to get latest hash repo may not exist or it may be private")
                continue

            sources.append(data)

with open('../index/index.json', 'w') as f:
    f.write(dumps(sources, indent=2))
