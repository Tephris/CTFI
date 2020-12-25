from CopyTextFromImage.ctfi import ScreenImageData

import unittest

class TestScreenData(unittest.TestCase):
	
	def test_normal_point_setting(self):
		data = ScreenImageData()
		data.pointA = (0, 0)
		data.pointB = (100, 100)

		self.assertTrue(data.pointA == (0, 0) and data.pointB == (100, 100))

	def test_pointB_set_before_pointA(self):
		data = ScreenImageData()
		
		with self.assertRaises(Exception) as context:
			data.pointB = (123, 123)

		self.assertTrue('pointA must be set before pointB.' in str(context.exception))

	def test_x_flip(self):
		data = ScreenImageData()
		data.pointA = (150, 150)
		data.pointB = (100, 250)

		self.assertTrue(data.pointA == (100, 150) and data.pointB == (150, 250))

	def test_y_flip(self):
		data = ScreenImageData()
		data.pointA = (100, 250)
		data.pointB = (150, 150)

		self.assertTrue(data.pointA == (100, 150) and data.pointB == (150, 250))

	def test_xy_flip(self):
		data = ScreenImageData()
		data.pointA = (150, 250)
		data.pointB = (100, 150)

		self.assertTrue(data.pointA == (100, 150) and data.pointB == (150, 250))


if __name__ == '__main__':
    unittest.main()