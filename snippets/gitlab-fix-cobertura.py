"""
Patch coverage.py XML report (Cobertura) to be supported by Gitlab CI.

> Note: The Cobertura XML parser currently does not support the sources element
> and ignores it. It is assumed that the filename of a class element contains
> the full path relative to the project root.
>
> - https://docs.gitlab.com/13.3/ee/user/project/merge_requests/test_coverage_visualization.html
"""

import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from pathlib import Path


parser = ArgumentParser()
parser.add_argument('--input')
parser.add_argument('--output')
args = parser.parse_args()

tree = ET.parse(args.input)
sources = [Path(s.text) for s in tree.find('sources')]
tree.getroot().remove(tree.find('sources'))

# for every `class`, change `filename` attribute to be a path
# relative to the project root instead of to `sources`.
for package in tree.find('packages'):
    for cls in package.find('classes'):
        fname = cls.attrib['filename']
        for src in sources:
            path = src.joinpath(fname)
            if path.exists():
                cls.attrib['filename'] = str(path)
                break
        else:
            raise RuntimeError(f'cannot find {fname}')

tree.write(args.output)
