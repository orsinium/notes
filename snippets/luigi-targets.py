"""
1. Universal base class for luigi targets.
2. Target for saving pandas.DataFrame to CSV file.
3. Target for saving numpy.array to CSV file.

Example:

```
target = DataFrameCSVTarget('path/to/file.csv')
with target.open('w') as stream:
    stream.write({'lol': 1, 'lal': 2})
with target.open('r') as stream:
    dataframe = stream.read()
```

"""

from contextlib import contextmanager
from pathlib import Path

import pandas
import numpy
from luigi import Target


class BaseTarget(Target):
    def exists(self):
        raise NotImplementedError

    @contextmanager
    def open(self, mode='rw'):
        try:
            yield self
        finally:
            if 'w' in mode:
                self.close()

    def read(self):
        raise NotImplementedError

    def write(self, data):
        raise NotImplementedError

    def close(self):
        pass


class DataFrameCSVTarget(BaseTarget):
    """Save pandas.DataFrame objects to one *.csv file.
    """
    def __init__(self, path, name=None):
        if isinstance(path, str):
            path = Path(path)
        if name is not None:
            path /= name + '.csv'
        self.path = path
        self.dataframe = pandas.DataFrame()

    def exists(self):
        return self.path.exists()

    def read(self):
        return pandas.read_csv(str(self.path))

    def write(self, data):
        self.dataframe.append(data)

    def close(self):
        self.dataframe.to_csv(str(self.path))


class NumPyCSVTarget(BaseTarget):
    """Save numpy.array to *.csv file.
    """
    def __init__(self, path, name=None):
        if isinstance(path, str):
            path = Path(path)
        if name is not None:
            path /= name + '.csv'
        self.path = path

    def exists(self):
        return self.path.exists()

    def read(self):
        return numpy.genfromtxt(str(self.path), delimiter=',')

    def write(self, data, header=None):
        delimiter = ','
        if isinstance(header, (list, tuple)):
            header = delimiter.join(header)
        numpy.savetxt(
            str(self.path),
            data,
            fmt='%.18e',
            delimiter=delimiter,
            newline='\n',
            header=header,
        )
