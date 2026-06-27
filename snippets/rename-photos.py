import os
from pathlib import Path
import re

rex = re.compile(r'PXL_(\d{8})_\d+\.jpg')

for path in Path().iterdir():
    matches = list(rex.finditer(path.name))
    if matches:
        new_stem = matches[0].group(1)
        new_name = f'{new_stem}.jpg'
        i = 1
        while Path(new_name).exists():
            i += 1
            new_name = f'{new_stem}-{i}.jpg'
        os.rename(path.name, new_name)
