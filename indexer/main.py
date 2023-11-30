import pathlib
from json import dumps

sources = []
for dir in pathlib.Path('../srcs').iterdir():
    if dir.is_dir():
        sources.append({"name": dir.name})

with open('../index/index.json', 'w') as f:
    f.write(dumps(sources, indent=2))
