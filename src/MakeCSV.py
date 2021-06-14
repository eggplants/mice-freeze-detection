from typing import Union


class MakeCSV():
    """Make a csv file of results.
    """

    def __init__(self, avi: str, delimiter: str = ',', header: bool = False,
                 out: Union[str, int] = 0, threshold: int = 30):
        """Constructor.

        Args:
            avi (str): video path
            delimiter (str, optional): delimiter separates value. Defaults to ','.
            header (bool, optional): flag if it inserts a header row. Defaults to False.
            out (Union[str, int], optional): output file path. Defaults to 0(stdout).
            threshold (int, optional): threshold for judging if a mice is freezing. Defaults to 30.
            window (bool, optional): flag if window is shown. Defaults to False.
        """
        self.avi = avi
        self.delimiter = delimiter
        self.header = header
        self.out = out
        self.threshold = threshold

    def make(self, res: list[int], bool_: list[int]) -> None:
        """Make CSV.
        """
        with open(self.out, 'w') as f:
            if self.header:
                print(self.delimiter.join(
                    ('frame_index', 'moving_dots', 'judge')), file=f)
            for ind, (r, b) in enumerate(zip(res, bool_)):
                vals = map(str, (ind, r, b))
                print(self.delimiter.join(vals), file=f)
