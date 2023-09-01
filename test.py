import numpy as np
import pandas as pd
import os
from pathlib import Path

x = np.array([[1, 2, 3], [4, 5, 6]], np.int32)
print(x)

full_path = os.path.abspath(__file__)
print(os.path.abspath(__file__))
parent_folder = str(Path(full_path).parents[0])
print(parent_folder)


