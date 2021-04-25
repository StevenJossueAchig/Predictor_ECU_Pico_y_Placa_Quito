import unittest
import requests
import os
from datetime import datetime
from src.pico_y_placa import PicoPlaca


class TestPicoYPlaca(unittest.TestCase):

    def test_invalid_plate(self):
        """
        Test that invalid plate raises ValueError
        """
        plate = 'A-123'
        now = datetime.now()
        date, tm = now.strftime("%Y-%m-%d %H:%M").split()
        with self.assertRaises(ValueError):
            result = PicoPlaca(plate, date, tm).predict()

    
    def test_invalid_date(self):
        """
        Test that invalid date raises ValueError
        """
        plate = 'EBA-0234'  # private vehicle
        now = datetime.now()
        date, tm = now.strftime("%d/%m/%Y %H:%M").split()
        with self.assertRaises(ValueError):
            result = PicoPlaca(plate, date, tm).predict()

    
    def test_invalid_time(self):
        """
        Test that invalid time raises ValueError
        """
        plate = 'EBA-0234'  # private vehicle
        now = datetime.now()
        date, tm = now.strftime("%Y-%m-%d %H:%M:%S").split()
        with self.assertRaises(ValueError):
            result = PicoPlaca(plate, date, tm).predict()

    
    def test_missing_key(self):
        """
        Test that missing API key raises requests.HTTPError
        """
        plate = 'EBA-0234'  # private vehicle
        now = datetime.now()
        date, tm = now.strftime("%Y-%m-%d %H:%M").split()
        try:
            del os.environ['HOLIDAYS_API_KEY']
        except KeyError:
            pass
        with self.assertRaises(requests.HTTPError):
            result = PicoPlaca(plate, date, tm, online=True).predict()


    def test_holiday(self):
        """
        Test that moved new holidays are restricted
        """
        date = '2021-04-30'  # Moved Labour Day, Friday
        plate = "EBA-0239"  # private vehicle prohibited on Fridays
        tm = '17:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)


    def test_holiday2(self):
        """
        Test that moved would-have-been holidays are not restricted
        """
        date = '2021-08-10'  # Would have been First Cry of Independence - moved, Tuesday
        plate = "EBA-0234"  # private vehicle prohibited on Tuesdays
        tm = '17:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertFalse(result)


    def test_holiday3(self):
        """
        Test that moved would-have-been continuous holidays are not restricted
        """
        date = '2021-11-03'  # Would have been Independence of Cuenca - moved, Wednesday
        plate = "EBA-0236"  # private vehicle prohibited on Wednesdays
        tm = '17:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertFalse(result)


    def test_weekend(self):
        """
        Test that weekends are not restricted
        """
        date = '2021-04-25'  # Sunday
        plate = 'EBA-0234'  # private vehicle
        tm = '17:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)


    def test_outside_peak_hours(self):
        """
        Test that time outside of not peak hours are not restricted
        """
        date = '2021-04-27'  # Tuesday
        plate = 'EBA-0234'  # private vehicle prohibited on Tuesdays
        tm = '20:00'  # outside peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)


    def test_vehicle(self):
        """
        Test that governemental vehicles are not restricted
        """
        date = '2021-04-27'  # Tuesday
        # Governmental vehicle, plate ending in 4 (normally restricted on Mondays)
        plate = 'AEC-0234'
        tm = '17:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)


    def test_vehicle2(self):
        """
        Test that diplomatic vehicles are not restricted
        """
        date = '2021-04-27'  # Tuesday
        # Governmental vehicle, plate ending in 4 (normally restricted on Mondays)
        plate = 'CD-0234'
        tm = '17:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)


    def test_restricted(self):
        """
        Test restricted case
        """
        date = '2021-04-27'  # Tuesday
        plate = 'EBA-0234'  # private vehicles' plates ending with 4 are restricted on Tuesdays
        tm = '17:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertFalse(result)
        

if __name__ == '__main__':
    unittest.main()
