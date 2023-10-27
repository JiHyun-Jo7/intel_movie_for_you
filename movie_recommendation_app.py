import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./movie_recommendation.ui')[0]
class Exam(QWidget, form_window):           # 클래스 생성
    def __init__(self):
        super().__init__()                  # 부모 클래스
        self.setupUi(self)





if __name__ == '__main__':                  # 메인
    app = QApplication(sys.argv)            # 객체 생성
    MainWindow = Exam()
    MainWindow.show()                       # 창를 화면에 출력
    sys.exit(app.exec_())                   # 창 화면 출력을 유지하는 함수