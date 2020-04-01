import cv2
import sys
from PySide2 import QtCore, QtGui, QtWidgets
import qimage2ndarray


class VideoPlayer(QtWidgets.QWidget):

    pause = False

    def __init__(self, width=640, height=480, fps=30):
        QtWidgets.QWidget.__init__(self)

        self.video_size = QtCore.QSize(width, height)
        self.camera_capture = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.frame_timer = QtCore.QTimer()

        self.setup_camera(fps)

        self.frame_label = QtWidgets.QLabel()
        self.file_dialog = QtWidgets.QFileDialog()
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.play_pause_button = QtWidgets.QPushButton("Pause")
        self.main_layout = QtWidgets.QVBoxLayout()

        self.setup_ui()

        QtCore.QObject.connect(self.play_pause_button, QtCore.SIGNAL("clicked()"), self.play_pause)

    def setup_ui(self):

        self.frame_label.setFixedSize(self.video_size)
        self.quit_button.clicked.connect(self.close_win)

        self.main_layout.addWidget(self.frame_label)
        #self.main_layout.addWidget(self.file_dialog)
        self.main_layout.addWidget(self.play_pause_button)
        self.main_layout.addWidget(self.quit_button)

        self.setLayout(self.main_layout)

    def play_pause(self):
        if not self.pause:
            print("stop")
            self.play_pause_button.setText("Play")
        else:
            print("start")
            self.play_pause_button.setText("Pause")
        self.pause = not self.pause

    def setup_camera(self, fps):
        self.camera_capture.set(3, self.video_size.width())
        self.camera_capture.set(4, self.video_size.height())

        self.frame_timer.timeout.connect(self.display_video_stream)
        self.frame_timer.start(int(1000 // fps))

    def display_video_stream(self):
        if not self.pause:
            ret, frame = self.camera_capture.read()

            if not ret:
                return False

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)

            image = qimage2ndarray.array2qimage(frame)
            self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def close_win(self):
        self.camera_capture.release()
        cv2.destroyAllWindows()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
