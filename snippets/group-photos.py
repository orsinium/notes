from datetime import datetime
import os
from pathlib import Path
from random import choice
import re
from string import ascii_lowercase
from PIL import Image

rex = re.compile(r'(PXL|IMG|VID)_(\d{8})_\d+\.(jpg|jpeg|mp4|3gp|avi)')
rex2 = re.compile(r'20[12]\d[01]\d{3}')
input_root = Path('input')
output_root = Path('output')


def get_date(path: Path) -> str | None:
    match = rex.fullmatch(path.name)
    if match:
        new_stem = match.group(2)
        return new_stem[:4] + '-' + new_stem[4:6]

    if path.suffix == '.jpg':
        exif = None
        try:
            exif = Image.open(path)._getexif()  # type: ignore
        except Exception:
            pass
        if exif:
            date = exif.get(36867)
            if date:
                return '-'.join(date.split(':')[:2])

    matches = rex2.findall(path.name)
    if len(matches) == 1:
        new_stem = matches[0]
        return new_stem[:4] + '-' + new_stem[4:6]

    try:
        dt = datetime.fromtimestamp(os.path.getmtime(path))
        return f'{dt.year}-{dt.month:02}'
    except Exception:
        pass

    return None


def add_suffix(path: Path) -> Path:
    suffix = ''.join(choice(ascii_lowercase) for _ in range(6))
    new_name = path.stem + '-' + suffix + path.suffix
    return path.parent / new_name


def main():
    for old_path in input_root.glob("**/*"):
        new_path = output_root
        if old_path.suffix.lower() in ('.jpg', '.jpeg'):
            new_path = new_path / 'photos'
        elif old_path.suffix.lower() in ('.mp4', '.3gp', '.avi'):
            new_path = new_path / 'videos'
        else:
            print(f'  not a photo: {old_path}')
            continue
        date = get_date(old_path)
        if not date:
            print(f'  no date: {old_path}')
            continue
        new_path = new_path / date / old_path.name
        new_path.parent.mkdir(parents=True, exist_ok=True)
        if new_path.exists():
            new_path = add_suffix(new_path)
        print(f'{old_path} -> {new_path}')
        os.rename(old_path, new_path)


main()
