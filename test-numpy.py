# . dev/bin/activate
# python3 -m pip install --upgrade pip
# pip install -r requirements.txt

import unittest
import math
import numpy as np
 
class Tests(unittest.TestCase):

    def test_matrix(self):

        # A vector times an array yields a vector
        a = np.array([1, 1])
        b = np.array([ [4, 1],
            [2, 2] ])
        c = np.matmul(a, b)
        self.assertIsNone(np.testing.assert_array_equal([6, 3], c))
        # Vector times a vector
        d = np.array([2, 2])
        e = np.matmul(c, d)
        self.assertEqual(18, e)

        # Transposing a 1D array does nothing
        self.assertIsNone(np.testing.assert_array_equal(a, np.transpose(a)))

        # Transposing a 2D array 
        bt = np.array([ [4, 2],
                        [1, 2] ])
        self.assertIsNone(np.testing.assert_array_equal(bt, np.transpose(b)))

if __name__ == '__main__':
    unittest.main()
