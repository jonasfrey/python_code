
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QDesktopWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot
from PIL.ImageQt import ImageQt 
from PIL import Image
import cv2

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # button = QPushButton('PyQt5 button', self)
        # button.setToolTip('This is an example button')
        # button.move(100,70)
        # button.clicked.connect(self.on_click)

        self.label = QLabel(self)
        self.pixmap = QPixmap('pil_red.png')
        self.label.setPixmap(self.pixmap)
        self.resize(self.pixmap.width(),self.pixmap.height())


        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')


# Convert an opencv image to QPixmap
def convertCvImage2QtImage(cv_img):
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    PIL_image = Image.fromarray(rgb_image).convert('RGB')
    return QPixmap.fromImage(ImageQt(PIL_image))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    monitor = QDesktopWidget().screenGeometry(0)

    ex = App()

    ex.move(monitor.left(), monitor.top())


    cap = cv2.VideoCapture(1)
    c = 0
    try:
        while True:
            c+=1
            ret, frame = cap.read()
            if(c % 2 == 0):
                ex.pixmap = QPixmap('my_fractal.png')
            else: 
                ex.pixmap = QPixmap('pil_red.png')
            #cv2.imshow("asdf", frame)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # image = QImage(frame,
            #     frame.shape[1],
            #     frame.shape[0],
            #     frame.strides[0],
            #     QImage.Format_RGB888)
            # ex.label.setPixmap(QPixmap.fromImage(image))
            # ex.show()
    except KeyboardInterrupt:
        print('interrupted!')

        cap.release()
        cv2.destroyAllWindows()


    sys.exit(app.exec_())

