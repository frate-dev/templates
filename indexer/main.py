import pathlib
from json import dumps, load

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
            try:
                latest_hash = get_latest_hash(data['git'])
            except Exception as e:
                print(f"Error: {file} failed to get latest hash repo may not exist or it may be private")
                continue
            if latest_hash:
                data['latest_hash'] = latest_hash

            sources.append(data)

with open('../index/index.json', 'w') as f:
    f.write(dumps(sources, indent=2))
