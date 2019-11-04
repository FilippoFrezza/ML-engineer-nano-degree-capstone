import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import pandas as pd


def test_min_amount(min_amount):
    test_df = pd.DataFrame({'col_1':[1,2,3,4,5,6,7,8,9,10], 'col_2':[1,2,3,4,5,6,7,None,None,None]})

    cols_to_remove = min_amount(test_df)
    assert cols_to_remove == ['col_2']
    print('test passed !')