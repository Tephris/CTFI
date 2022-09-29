import clipboard
import os
import pytesseract
import sys
import win32api
import win32gui
from PIL import ImageGrab
from pynput.mouse import Controller
from pynput import keyboard

# Add any other supported language you want in (Display Name, Language Code) format
# Language codes must match the traineddata file names found in the Tesseract-OCR/tessdata/ folder
languages = [
	('Chinese Simplified', 'chi_sim'),
	('Chinese Traditional', 'chi_sim'),
	('English', 'eng'),
	('Japanese', 'jpn'),
	('Korean', 'kor')
]

languages = dict((i + 1, l) for i, l in enumerate(languages))

class ScreenImageData:
	def __init__(self, x1=0, y1=0, x2=0, y2=0):
		self.__pointA = (x1, y1)
		self.__pointB = (x2, y2)
		self.isPointASet = False
		self.currentMousePosition = (0, 0)
		self.windowHandles = set()

	@property
	def pointA(self):
		return self.__pointA
	
	@property
	def pointB(self):
		return self.__pointB
	
	@pointA.setter
	def pointA(self, pointA):
		self.__pointA = (pointA[0] if pointA[0] > 0 else 0, pointA[1] if pointA[1] > 0 else 0)
		self.isPointASet = True

	@pointB.setter
	def pointB(self, pointB):
		if not self.isPointASet:
			raise Exception("pointA must be set before pointB.")

		if self.pointA == pointB:
			self.isPointASet = False

		self.__pointB = (pointB[0] if pointB[0] > 0 else 0, pointB[1] if pointB[1] > 0 else 0)

		if self.__pointA[0] > self.__pointB[0]:
			self.__pointA, self.__pointB = (self.__pointB[0], self.__pointA[1]), (self.__pointA[0], self.__pointB[1])

		if self.__pointA[1] > self.__pointB[1]:
			self.__pointA, self.__pointB = (self.__pointA[0], self.__pointB[1]), (self.__pointB[0], self.__pointA[1])

def clearScreens(screenImageData):
	for hwnd in screenImageData.windowHandles:
		win32gui.InvalidateRect(hwnd, None, True)

def onPress(mouseController, screenImageData, showBox):
	red = win32api.RGB(255, 0, 0)
	deviceContext = win32gui.GetDC(None)

	def callback(key):
		if key is key.shift and not screenImageData.isPointASet:
			screenImageData.pointA = mouseController.position

		if showBox:
			if screenImageData.currentMousePosition != mouseController.position:
				screenImageData.windowHandles.add(win32gui.WindowFromPoint(mouseController.position))
				clearScreens(screenImageData)
				screenImageData.currentMousePosition = mouseController.position

			if screenImageData.isPointASet:
				minX = min(screenImageData.pointA[0], mouseController.position[0])
				maxX = max(screenImageData.pointA[0], mouseController.position[0])
				minY = min(screenImageData.pointA[1], mouseController.position[1])
				maxY = max(screenImageData.pointA[1], mouseController.position[1])

				for x in range(maxX - minX):
					win32gui.SetPixel(deviceContext, minX + x, minY, red)
					win32gui.SetPixel(deviceContext, minX + x, maxY, red)

				for y in range(maxY - minY):
					win32gui.SetPixel(deviceContext, minX, minY + y, red)
					win32gui.SetPixel(deviceContext, maxX, minY + y, red)

	return callback

def onRelease(mouseController, screenImageData):
	def callback(key):
		clearScreens(screenImageData)
		if key is key.shift:
			screenImageData.pointB = mouseController.position
			# Return false to stop keyboard listener
			return False

	return callback


def main():
	showBox = True
	if len(sys.argv) > 1 and (sys.argv[1] == "-h" or sys.argv[1] == "--hide"):
		showBox = False

	directory = os.path.dirname(__file__)
	mouse = Controller()
	selection = ScreenImageData()

	pytesseract.pytesseract.tesseract_cmd = '{}\\Tesseract-OCR\\tesseract.exe'.format(directory)
	tessdata_dir_config = '--tessdata-dir "{}\\Tesseract-OCR\\tessdata"'.format(directory)

	languageSelection = 0
	while languageSelection == 0:
		try:
			for i in range(1, len(languages) + 1):
				print('#{} - {}'.format(i, languages[i][0]))
			selectedLanguage = int(input('\nSelect a language: #'))
			if selectedLanguage in languages:
				languageSelection = selectedLanguage
			else:
				raise Exception
		except:
			print('Invalid input provided. Please try again ...\n')

	while selection.pointA == selection.pointB:
		print('Press and hold shift to start selection. Release shift to confirm selection ...')
		with keyboard.Listener(
				on_press=onPress(mouse, selection, showBox),
				on_release=onRelease(mouse, selection)) as listener:
			listener.join()

		if selection.pointA == selection.pointB:
			print('The start point and end point of the selection cannot be the same. Please try again ...\n')

	try:
		# Add 1 to pointA to account for selection indicator box
		img = ImageGrab.grab(bbox=(selection.pointA[0] + 1, selection.pointA[1] + 1, *selection.pointB), include_layered_windows=False, all_screens=True)
		
		# Convert selected image to greyscale to improve character recognition
		img = img.convert('L')

		# The last character of the string is ignored when copying to clipboard due to it being a null character representing the end of the string
		clipboard.copy(pytesseract.image_to_string(img, lang=languages[languageSelection][1], config=tessdata_dir_config)[:-1])
	except Exception as err:
		print('\nERROR:', err)
		input('\nPress Enter to exit...')

if __name__ == '__main__':
	main()