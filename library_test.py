import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    def test_integers_with_commas_billions(self):
        self.assert_extract("I make 3,123,456,789 a year", library.integers, "3,123,456,789")

    def test_integers_with_commas_billions_2(self):
        self.assert_extract("I make 23,123,456,789 a year", library.integers, "23,123,456,789")

    def test_integers_with_commas_billions_3(self):
        self.assert_extract("I make 123,123,456,789 a year", library.integers, "123,123,456,789")

    def test_integers_with_commas_millions(self):
        self.assert_extract("I make 123,456,789 a year", library.integers, "123,456,789")

    def test_integers_with_commas_millions_2(self):
        self.assert_extract("I make 12,345,678 a year", library.integers, "12,345,678")

    def test_integers_with_commas_millions_3(self):
        self.assert_extract("I make 1,234,567 a year", library.integers, "1,234,567")

    def test_integers_with_missing_some_commas_millions(self):
        self.assert_extract("I make 123,456,789 a year", library.integers, "123,456,789")

    def test_integers_with_commas_thousand(self):
        self.assert_extract("I make 12,345 a year", library.integers, "12,345")

    def test_integers_with_commas_thousand_second(self):
        self.assert_extract("I make 1,234 a year", library.integers, "1,234")

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    def test_invalid_date(self):
        self.assert_extract("I was born 2016-13-22", library.dates_iso8601)
        self.assert_extract("I was born 2017-11-32", library.dates_iso8601)

    def test_date_iso8601_extract(self):
        self.assert_extract("I was born on 2015-07-25", library.dates_iso8601, '2015-07-25')

    def test_named_date_extract(self):
        self.assert_extract("I was born on 25 Jan 2018", library.dates_named, '25 Jan 2018')

    def test_date_iso8601_with_valid_timestamp_T_hour_minute(self):
        self.assert_extract("This test was completed at 2018-06-22T18:22", library.dates_iso8601, '2018-06-22T18:22')

    def test_date_iso8601_with_valid_timestamp_space_hour_minute(self):
        self.assert_extract("This test was completed at 2018-06-22 18:22", library.dates_iso8601, '2018-06-22 18:22')

    def test_date_iso8601_with_valid_timestamp_T_hour_minute_second(self):
        self.assert_extract("This test was completed at 2018-06-22T18:22:19", library.dates_iso8601, '2018-06-22T18:22:19')

    def test_date_iso8601_with_valid_timestamp_space_hour_minute_second_millisecond(self):
        self.assert_extract("This test was completed at 2018-06-22 18:22:19.012", library.dates_iso8601, '2018-06-22 18:22:19.012')

    def test_date_iso8601_with_valid_timestamp_T_three_abr_timezone(self):
        self.assert_extract("This test was completed at 2018-06-22T18:22:19.123 MDT", library.dates_iso8601, '2018-06-22T18:22:19.123 MDT')

    def test_date_iso8601_with_valid_timestamp_space_three_abr_timezone(self):
        self.assert_extract("This test was completed at 2018-06-22 18:22:19.123 PDS", library.dates_iso8601, '2018-06-22 18:22:19.123 PDS')

    def test_date_iso8601_with_valid_timestamp_T_single_letter_timezone(self):
        self.assert_extract("This test was completed at 2018-06-22T18:22:19.123 Z", library.dates_iso8601, '2018-06-22T18:22:19.123 Z')

    def test_date_iso8601_with_valid_timestamp_space_single_letter_timezone(self):
        self.assert_extract("This test was completed at 2018-06-22 18:22:19.123 D", library.dates_iso8601, '2018-06-22 18:22:19.123 D')

    def test_date_iso8601_with_valid_timestamp_T_negative_offset(self):
        self.assert_extract("This test was completed at 2018-06-22T18:22:19.123 -0700", library.dates_iso8601, '2018-06-22T18:22:19.123 -0700')

    def test_date_iso8601_with_valid_timestamp_space_positive_offset(self):
        self.assert_extract("This test was completed at 2018-06-22 18:22:19.123 +1200", library.dates_iso8601, '2018-06-22 18:22:19.123 +1200')

    def test_date_iso8601_with_invalid_timestamp(self):
        self.assert_extract("At 2018-06 22 18:22 I fell asleep", library.dates_iso8601)

    def test_named_date_with_commas(self):
        self.assert_extract("This new date 20 Jun, 2018 should work", library.dates_named, "20 Jun, 2018")

if __name__ == '__main__':
    unittest.main()
