# . dev/bin/activate
# pip install pandas

import unittest
import pandas as pd
import math
import numpy as np
 
 
class Tests(unittest.TestCase):

    def test_filter(self):
        obj = pd.Series([4, 5, 10], index=["a", "b", "c"])
        obj = obj[obj >= 5]
        self.assertEqual(2, obj.size)

    def test_sum(self):
        # Take two series with common index values and join them
        s1 = pd.Series([1, 2], index=['A', 'B'], name='s1')
        s2 = pd.Series([3, 4], index=['A', 'B'], name='s2')
        s3 = pd.concat([s1, s2], axis=1)
        self.assertEqual(3, s3["s1"].sum())
        

    def test_join(self):
        # Take two series with common index values and join them
        s1 = pd.Series([1, 2], index=['A', 'B'], name='s1')
        s2 = pd.Series([3, 4], index=['A', 'B'], name='s2')
        s3 = pd.concat([s1, s2], axis=1)
        self.assertEqual(2, s3["s1"].size)
        self.assertEqual(2, s3["s2"].size)

        # Take two series with common index values and join them.  Notice
        # in this case the second series is missing a value.  This 
        # will result in a NaN (i.e. an outer join)
        s1 = pd.Series([1, 2, 6], index=['A', 'B', 'C'], name='s1')
        s2 = pd.Series([3, 4], index=['A', 'B'], name='s2')
        s3 = pd.concat([s1, s2], axis=1)
        self.assertEqual(3, s3["s2"].size)
        """
           s1   s2
        A   1  3.0
        B   2  4.0
        C   6  NaN
        """

        # Take two series with common index values and join them.  Notice
        # in this case the second series is missing a value.  This 
        # will result in shortened result (inner)
        s1 = pd.Series([1, 2, 6], index=['A', 'B', 'C'], name='s1')
        s2 = pd.Series([3, 4], index=['A', 'B'], name='s2')
        s3 = pd.concat([s1, s2], axis=1, join='inner')
        self.assertEqual(2, s3["s2"].size)
        """
           s1  s2
        A   1   3
        B   2   4
        """

        # Filtering 
        s1 = pd.Series([1, 2, 6], index=['A', 'B', 'C'], name='s1')
        s2 = pd.Series([3, 4, 7], index=['A', 'B', 'C'], name='s2')
        s3 = pd.concat([s1, s2], axis=1)
        # Here we create a boolean vector from one of the series and then 
        # use it to index the DataFrame.
        s4 = s3[s3["s1"] >= 2]
        self.assertEqual(2, s4["s2"].size)
 

    # A Series is a fixed-length, ordered dictionary
    def test_series_1(self):
 
        obj = pd.Series([4, 5, 10])
        self.assertEqual(3, obj.size)
        # By default the index is a range from 0..3
        self.assertEqual(0, obj.index[0])
        # Lookup an item using the index
        self.assertEqual(10, obj[2])
 
        # Create a series with an identifying index
        obj1 = pd.Series([4, 5, 10], index=[1, 2, 3])
        # Access an item in the index
        self.assertEqual(1, obj1.index[0])
        # Access series data using the index
        self.assertEqual(10, obj1[3])
 
        # Notice that the index doesn't need to be a number
        obj2 = pd.Series([4, 5, 10], index=["a", "b", "c"])
        # Access an item in the index
        self.assertEqual("a", obj2.index[0])
        # Access series data using the index
        self.assertEqual(10, obj2["c"])
 
        # Notice that the index is preserved when we do vector operations:
        obj3 = obj2 * 2
        # Access series data using the index
        self.assertEqual(20, obj3["c"])
 
        # Creating a series using a dictionary
        d4 = {"a": 4, "b": 5, "c": 10}
        series4 = pd.Series(d4)
        # Access series data using the index
        self.assertEqual(10, series4["c"])
 
        # Showing alignment.  We create a series that uses the same index
        # values, but in a different order
        d5 = {"c": 2, "b": 9, "a": 10, "d": 7}
        series5 = pd.Series(d5)
        # Now add the two series
        series6 = series4 + series5
        # Notice that the common entries were added
        self.assertEqual(12, series6["c"])
        # Notice that the place where we had a disconnect resulted in a NaN, NOT A ZERO!
        self.assertTrue(math.isnan(series6["d"]))
 
        # A few basic statistics
        self.assertAlmostEqual(7, series5.mean())
        # Pandas standard deviation (using sample)
        self.assertAlmostEqual(3.55, series5.std(), 1)
        # Notice that this is different (using population)
        self.assertAlmostEqual(3.08, np.std(series5), 1)
 
        # Showing that we can name the index and data
        series5.index.name = "Test Index"
        series5.name = "Test Data"
 
    # Showing what datetime indices look like (time series)
    def test_series_2(self):
        # Here's what a time series looks like
        dti = pd.to_datetime(["1/1/2021", "1/2/2021"])
        # Notice that this function is able to deal with a lot of different formats
        dti2 = pd.to_datetime(["1/1/2021", "2021-01-02", np.datetime64("2021-01-03")])
        self.assertEqual(np.datetime64("2021-01-03"), dti2[2])
        # Create a series using the dates provided
        series1 = pd.Series([4, 5, 10], index=dti2)
        # Look up by date
        self.assertEqual(10, series1[np.datetime64("2021-01-03")])
        # Check key in index
        self.assertTrue(np.datetime64("2021-01-03") in series1.index)
        self.assertFalse(np.datetime64("2021-01-04") in series1.index)
 
    # Demonstrate filtering a series using a set of specific dates and with
    # a mask series
    def test_series_3(self):
        dti = pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"])
        # Create a series using the dates provided
        series1 = pd.Series([4, 5, 10, 11, 7], index=dti)
        # Look up by date
        self.assertEqual(10, series1[np.datetime64("2021-01-03")])
        # Check key in index
        self.assertTrue(np.datetime64("2021-01-03") in series1.index)
        self.assertFalse(np.datetime64("2021-01-06") in series1.index)
 
        # Demonstrate filtering a series by index
        dti2 = pd.to_datetime(["2021-01-04", "2021-01-05"])
        self.assertEqual(2, series1[dti2].index.size)
 
        self.assertEqual(5, len(series1.index))
        self.assertEqual(np.datetime64("2021-01-03"), series1.index[2])
        # Looking at a part of an index (first two elements)
        self.assertEqual(np.datetime64("2021-01-02"), series1.index[:2][1])
 
        # Filter an index to find weekdays
        filtered_index = list(filter(lambda x: x.dayofweek < 5, series1.index))
        self.assertEqual(3, len(filtered_index))
        # Filter the original series using the reduced index members
        self.assertEqual(3, series1[filtered_index].index.size)
 
    # DataFrames are similar to a dictionary of Series, all sharing the same index
    def test_dataframe_1(self):
        dti = pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03"])
        # Dictionary of equal-length lists
        data = {
            "s0": [4, 5, 10],
            "s1": [6, 2, 1]
        }
        df1 = pd.DataFrame(data, index=dti)
        self.assertEqual(10, df1["s0"][np.datetime64("2021-01-03")])
        # See how the indices are preserved
        s2 = df1["s0"] + df1["s1"]
        self.assertEqual(11, s2[np.datetime64("2021-01-03")])
        # Adding another column to the existing dataframe
        df1["s2"] = df1["s0"] + df1["s1"]
        self.assertEqual(11, df1["s2"][np.datetime64("2021-01-03")])
 
        # Statistical measures will result in a dictionary, one entry for
        # each series (column) that was aggregated by the std() operation
        self.assertEqual("s0", df1.std().keys()[0])
 
        # Filtering example
        bool_series = df1["s0"] >= 5
        self.assertEqual(3, bool_series.size)
        # This is a boolean vector
        self.assertEqual("bool", bool_series.dtype)
 
        # Sum the DF using the boolean series as a filter
        self.assertEqual(3, df1[bool_series]["s1"].sum())
 
    def test_dataframe_2(self):
        dti = pd.to_datetime(["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"])
        # Dictionary of equal-length lists
        data = {
            "s0": [4, 5, 10, 1, 2]
        }
        df1 = pd.DataFrame(data, index=dti)
 
        # Show quantiles
        #print(pd.qcut(df1['s0'], 2, labels=False))
  
if __name__ == '__main__':
    unittest.main()