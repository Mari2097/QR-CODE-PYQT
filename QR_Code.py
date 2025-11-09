from PyQt6.QtGui import QImage ,QPixmap 
from PyQt6.QtCore import QTimer , Qt 
from PyQt6.QtWidgets import QApplication, QWidget ,QMessageBox ,QVBoxLayout ,QPushButton ,QLabel
import cv2
import sys



try :
    from pyzbar.pyzbar import decode
except ImportError:
    print("Warning : pyzbar not find . please run : pip install pyzbar")
    decode =None
    

class QRCodeScannerApp(QWidget):
    def __init__(self):
       super().__init__()
       self.setWindowTitle("QR _ CODE _ SCANNER")
       self.setGeometry(100,100,640,480 ) # (x, y, width, height)
       
       
       if decode is None:
           QMessageBox.critical(self ,"ERROR" ," please run : pip install pyzbar")
           self.close()
           return
       
       self.cap = None
       self.timer =QTimer()
       self.timer.timeout.connect(self.update_frame)
       
       self.setup_ui()
       
       
    def setup_ui(self):
        
        layout =QVBoxLayout()
        
        self.video_label =QLabel()
        self.video_label.setFixedSize(600 , 480)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setText("پنجره نمایش دوربین")
        layout.addWidget(self.video_label)
        
        self.start_button = QPushButton("شروع اسکن")
        self.start_button.clicked.connect(self.toggle_scan)
        layout.addWidget(self.start_button)
        
        self.setLayout(layout)
        
        
    def toggle_scan(self):
        
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                QMessageBox.critical(self , "خطا","دوربین یافت نشد یا قابل دسترسی نیست ")
                return
            self.timer.start(30)  # هر ۳۰ میلی‌ثانیه فریم جدید
            self.start_button.setText("توقف اسکن")
            
        else:
            
            self.timer.stop()
            if self.cap:
                self.cap.release()
            self.video_label.setText("اسکن متوقف شد")
            self.start_button.setText("شروع اسکن")
            
            
    def update_frame(self):
        """دریافت فریم جدید و نمایسش ان و اسکن کد"""
        ret , frame =self.cap.read()
        
        if ret:
            rgbImage = cv2.cvtColor(frame ,cv2.COLOR_BGR2RGB)
            h,w,ch =rgbImage.shape
            bytesPerLine = ch* w
            
            convertToImage =QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            pixmap =QPixmap.fromImage(convertToImage)
            
            self.video_label.setPixmap(pixmap.scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
            
            decode_objects =decode(frame)
            
            for obj in decode_objects:
                data =obj.data.decode('utf-8')
                format_name =obj.type
                
                QMessageBox.information(
                    self,
                    "کد شناسایی شد" ,
                   
                    f"فرمت :{format_name}\nداده: {data} "
                    
                )
                self.toggle_scan()
                break
            
            
    def closeEvent(self, event):
        """اطمینان از بسته شدن دوربین هنگام خروج"""
        self.timer.stop()
        if self.cap:
            self.cap.release()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QRCodeScannerApp()
    window.show()
    sys.exit(app.exec())