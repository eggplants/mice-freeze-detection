from typing import Union

from DetectFreezing import DetectFreezing


class MakeCSV():
    def __init__(self, avi: str, delimiter: str = ',', header: bool = False,
                 out: Union[str, int] = 0, threshold: int = 10,
                 window: bool = False):
        self.avi = avi
        self.delimiter = delimiter
        self.header = header
        self.out = out
        self.threshold = threshold
        self.window = window

    def make(self) -> None:
        d = DetectFreezing(self.avi)
        res: list[int] = d.detect(show_window=self.window)
        b = d.convert_boolean_with_threshold(res, self.threshold)

        with open(self.out, 'w') as f:
            if self.header:
                print(self.delimiter.join(
                    ('frame_index', 'moving_dots', 'judge')), file=f)
            for ind, (r, b) in enumerate(zip(res, b)):
                vals = map(str, (ind, r, b))
                print(self.delimiter.join(vals), file=f)
