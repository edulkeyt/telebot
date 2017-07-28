import sys, cv2 as cv
import serial


SERIAL_PORT = 'COM3';
SERIAL_BAUD_RATE = 9600;
CLASSIFICATOR_PATH = "C:\\opencv\\build\\etc\\lbpcascades\\lbpcascade_frontalface.xml"
PICTURE_WIDTH = 640
PICTURE_HEIGHT = 480

cap = cv.VideoCapture(0) 
cascade = cv.CascadeClassifier(CLASSIFICATOR_PATH)# Загрузка обученного каскадного классификатора 

ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD_RATE)
angles = [90, 90, 90, 90]

def calculateDelta(targetValue, actualValue):
 if -20 < targetValue - actualValue < 20:
  return 0;
 if targetValue < actualValue:
  return 1;
 if targetValue > actualValue:
  return -1;

def sendAngles(deltaX, deltaY):
 global angles;
 angles[0] += deltaX;
 angles[1] += deltaY;
 ser.write(bytes([int(angles[0]), int(angles[1]), int(angles[2]), int(angles[3])]));

def handleDetectedResult(img, x, y, w, h): 
 cv.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2) # Вокруг найденного лица рисуем красный прямоугольник
 sendAngles(calculateDelta(x+(w/2), PICTURE_WIDTH/2), calculateDelta(PICTURE_HEIGHT/2, y+(h/2)));
 

def detect(img):
 gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
 sf = min(PICTURE_WIDTH/img.shape[1], PICTURE_HEIGHT/img.shape[0]) 
 gray = cv.resize(gray, (0,0), None, sf, sf) # Масштабирование
 
 rects = cascade.detectMultiScale(gray, scaleFactor=1.1, 
  minNeighbors=4, minSize=(40, 40), 
  flags=cv.CASCADE_SCALE_IMAGE) # Детектирование 

 gray = cv.GaussianBlur(gray, (3, 3), 1.1) # Размываем 
 edges = cv.Canny(gray, 5, 50) # Детектируем ребра 
 
 out = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
 
 for x, y, w, h in rects: 
  handleDetectedResult(img, x, y, w, h)

 cv.imshow("edges+face", img)
 cv.waitKey(30)

while True:
 ok, img = cap.read() 
 if not ok: 
  break 
 detect(img)

 
