import pathlib
from json import dumps, load

sources = []
for dir in pathlib.Path('../srcs').iterdir():
    if dir.is_dir():
        file = pathlib.Path(dir)/'index.json'
        if not (file.exists()):
            print(f"Warning: {file} does not exist")
        with open(file, 'r') as f:
            sources.append(load(f))

with open('../index/index.json', 'w') as f:
    f.write(dumps(sources, indent=2))
