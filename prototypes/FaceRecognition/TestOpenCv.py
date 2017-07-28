import sys, cv2 as cv

cap = cv.VideoCapture(0) 
cascade = cv.CascadeClassifier("C:\\opencv\\build\\etc\\lbpcascades\\lbpcascade_frontalface.xml")# Загрузка обученного каскадного классификатора 

def handleDetectedResult(img, x, y, w, h):
 cv.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2) # Вокруг найденного лица рисуем красный прямоугольник

def detect(img):
 gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) 
 sf = min(640./img.shape[1], 480./img.shape[0]) 
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

 
