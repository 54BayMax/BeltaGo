# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import pyqtSignal
import webbrowser
from Ui_BgGui import Ui_MainWindow
from PyQt4.QtGui import QMovie,QTextCursor
from BgAudio import *
import data
from std_msgs.msg import String
import rospy
import os
import time, json
import PIL.Image as PImage
from PIL.ImageQt import ImageQt
#import io
import signal
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import time,threading

qImg=None
Lock=threading.Lock()

class MainWindow(QMainWindow, Ui_MainWindow,threading.Thread):
    """
    Class documentation goes here.
    """
    #image_trigger=pyqtSignal(QImage)

    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        threading.Thread.__init__(self)
        self.name=self.voice_tts.__name__
        self.setupUi(self)
        self.framerate = 8000
        self.NUM_SAMPLES = 2000
        self.channels = 1
        self.sampwidth = 2
        self.TIME = 2
        self.file_name_index = 1
        self.LEVEL = 700
        self.mute_begin = 0
        self.mute_count_limit = 200
        self.mute_end = 1
        self.not_mute = 0
        self.wav_queue = Queue.Queue(1024)
        self.voice_queue = Queue.Queue(1024)
        self.image_queue=Queue.Queue()
        self.thread_flag = 0
        self.start_flag = 1
        self.mydata=data.data()
        self.oldImage=QPixmap()
        #ROS 
        self.car_speed=28
        self.dir='S'
        self.carpub=rospy.Publisher("carController",String,queue_size=3)
        self.armpub=rospy.Publisher("armController",String,queue_size=3)
        #self.controlpub=rospy.Publisher("", String, queue_size=3)
        self.armsub=rospy.Subscriber("armMsg", String, self.armCallBack)
        self.image_sub = rospy.Subscriber("/image_converter/rgb",Image,self.imageCallback)
        self.armlock=0
        
        #self.connect(self, QtCore.SIGNAL('image_trigger'), self.drawImage)
        self.servo=0
        self.bridge = CvBridge()
        self.timer=QtCore.QBasicTimer()
        
        #Ros 
        self.armx=0
        self.army=-18
        self.armz=10
        self.pump=0

        
    def timerEvent(self, event):
        global qImg
        try:
            Lock.acquire()
            pixImg=QPixmap.fromImage(qImg)
            self.playlabel.setPixmap(pixImg)
            Lock.release()
        except:
            pass
        



    def armCallBack(self, msg):
        data=str(msg)[6:]
        json_data=json.loads(data)
        flag=int(json_data['state'])
        self.armlock=int(json_data['lock'])
        error=int(json_data['error'])
        error_value=int(json_data['error_value'])
        if self.armlock:
            QMessageBox.about(self, u'warniing', u'arm is moving')
        if flag == 1:
            QMessageBox.about(self, u'result', u'Success')
        elif flag == -1:
            QMessageBox.about(self, u'result', u'Fail')
        else:
            pass
        
        print error, error_value
            
    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.voice_tts,())
        print self.name, 'finished it:', ctime()

    def writeQ(self, queue, data):
        queue.put(data, 1)

    def readQ(self, queue):
        val = queue.get(1)
        return val

    def getResult(self):
        return self.res

    def voice_tts(self):
        self.use_cloud(token=self.get_token())

    def get_token(self):
        apiKey = "h2fAPxonRVm8e59GMojhpEH8"
        secretKey = "d55e1e38ea4932e78bf4abac3def1401"
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
        res = urllib2.urlopen(auth_url)
        json_data = res.read()
        print 'json_data:', type(json_data)
        return json.loads(json_data)['access_token']
    
    def dump_res(self, buf):
        my_temp = json.loads(buf)
        if my_temp['err_no']:
            if my_temp['err_no'] == 3300:
                self.textBrowser.append(u'输入错误')
            elif my_temp['err_no'] == 3301:
                 self.mydata.speak(u'人家没听清楚啦')
            elif my_temp['err_no'] == 3302:
                self.textBrowser.append(u'验证错误')
            elif my_temp['err_no'] == 3303:
                self.textBrowser.append(u'服务错误')
            elif my_temp['err_no'] == 3304:
                self.textBrowser.append(u'单日申请GPS过大')
            elif my_temp['err_no'] == 3305:
                self.textBrowser.append(u'请求次数太多')
        else:
            my_list = my_temp['result']
            self.textBrowser.append(my_list[0][:-1])
            self.textBrowser.moveCursor(QTextCursor.End)
            tmp=u' 语音消息:%s'%(my_list[0][:-1])
            re=u'%s'%(my_list[0][:-1])
            self.car_speed, self.dir, self.servo=self.mydata.dealWithData(re, self.car_speed, self.dir, self.servo)
  #          print self.car_speed, self.dir, self.servo
            self.sendCarMsg()
            str=self.mydata.normal_data(tmp)
            self.textBrowser_2.append(str)
            self.textBrowser_2.moveCursor(QTextCursor.End)
            
            
    def use_cloud(self, token):
        while True:
            if self.wav_queue.qsize():
                filename = self.readQ(queue=self.wav_queue)
            else:
                continue
            fp = wave.open(filename, 'rb')
            nf = fp.getnframes()  # 获得文件采样点数量
            # print 'self.sampwidth:',fp.getsampwidth()
            # print 'framerate:',fp.getframerate()
            # print 'self.channels:',fp.getnchannels()
            f_len = nf * 2  # 文件长度计算，每个采样点2字节
            audio_data = fp.readframes(nf)

            cuid = "xxxxxxxxx"  #
            srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
            http_header = [
                'Content-Type:audio/pcm;rate=8000',
                'Content-Length:%d' % f_len
            ]

            c = pycurl.Curl()
            c.setopt(pycurl.URL, str(srv_url))
            c.setopt(c.HTTPHEADER, http_header)
            c.setopt(c.POST, 1)
            c.setopt(c.CONNECTTIMEOUT, 80)
            c.setopt(c.TIMEOUT, 80)
            c.setopt(c.WRITEFUNCTION, self.dump_res)
            c.setopt(c.POSTFIELDS, audio_data)
            c.setopt(c.POSTFIELDSIZE, f_len)
            try:
                c.perform()
            except Exception as e:
                print e
            sleep(0.1)

    def record_wave(self,temp):
        while self.start_flag == 1:
            pa = PyAudio()
            stream = pa.open(format=paInt16, channels=1, rate=self.framerate, input=True,
                             frames_per_buffer=self.NUM_SAMPLES)
            save_buffer = []
            count = 0
            while count < self.TIME * 20:
                string_audio_data = stream.read(self.NUM_SAMPLES)
                audio_data = np.fromstring(string_audio_data, dtype=np.short)
                large_sample_count = np.sum(audio_data > self.LEVEL)
                print large_sample_count
                if large_sample_count < self.mute_count_limit:
                    self.mute_begin = 1
                else:
                    save_buffer.append(string_audio_data)
                    self.mute_begin = 0
                    self.mute_end = 1
                count += 1
                if (self.mute_end - self.mute_begin) > 9:
                    self.mute_begin = 0
                    self.mute_end = 1
                    break
                if self.mute_begin:
                    self.mute_end += 1
                print '.'
            save_buffer = save_buffer[:]
            if save_buffer:
                if self.file_name_index < 11:
                    pass
                else:
                    self.file_name_index = 1
                filename = str(self.file_name_index) + '.wav'
                self.save_wave_file(filename=filename, data=save_buffer)
                self.writeQ(queue=self.wav_queue, data=filename)
                self.file_name_index += 1
                print filename, 'saved'
            else:
                print 'file not saved!'
            # self.save_wave_file('01.wav',my_buf)
            save_buffer = []
            stream.close()
            
    def imageCallback(self, msg):
        global qImg
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
            cv_image=cv2.resize(cv_image, (640, 480))
            image=PImage.frombytes("RGB", (640, 480), cv_image.tostring())
            Lock.acquire()
            qImg=ImageQt(image)
            Lock.release()

        except CvBridgeError as e:
            print 'a'
            print(e)

    def save_wave_file(self, filename, data):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes("".join(data))
        wf.close()
        
    def sendCarMsg(self):
        data='{"speed":%d,"dir":"%s","servo":%d,"depth":0,"debug":1}'%(int(self.car_speed),self.dir,int(self.servo))
        if not rospy.is_shutdown():
            self.carpub.publish(String(data))
            
    def sendArmMsg(self):
        data='{"x":%d,"y":%d,"z":%d,"p":%d,"debug":%d}'%(self.armx,self.army,self.armz,self.pump,1)
        if not rospy.is_shutdown():
            self.armpub.publish(String(data))
    
    @pyqtSignature("")
    def on_actionAbout_us_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        my_button=QMessageBox.about(self, u'关于我们', u'BeltaGo致力于以一种全新的形式，来体现作者的洪荒之力。')
    
    @pyqtSignature("bool")
    def on_actionHow_to_use_triggered(self, checked):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        webbrowser.open('www.baidu.com')
    
    @pyqtSignature("")
    def on_actionContact_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        my_button=QMessageBox.about(self, u'联系方式', u'QQ:876954540 Tel:15002963163')
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, u'退出BeltaGo?',
        u'你真的真的真的确定要退出?', QtGui.QMessageBox.Yes,
        QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    @pyqtSignature("")
    def on_pButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.timer.start(50, self)
            
    @pyqtSignature("")
    def on_pushButton_5_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_5.setStyleSheet('border-radius:10px;color:#DDDDDD;background-color:#44FFFF;font-weight:bold;')
        str=self.mydata.button_data(u' 方向:右')
        self.textBrowser_2.append(str)
        self.textBrowser_2.moveCursor(QTextCursor.End)
        self.dir="L"
        self.sendCarMsg()
        
    @pyqtSignature("")
    def on_pushButton_5_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_5.setStyleSheet('border-radius:10px;color:white;background-color:#00FFFF;font-weight:bold;')

    @pyqtSignature("")
    def on_pushButton_7_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_7.setStyleSheet('border-radius:10px;color:#DDDDDD;background-color:#44FFFF;font-weight:bold;')
        str=self.mydata.button_data(u' 方向:下')
        self.textBrowser_2.append(str)
        self.textBrowser_2.moveCursor(QTextCursor.End)
        self.dir="D"
        self.sendCarMsg()
    
    @pyqtSignature("")
    def on_pushButton_7_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_7.setStyleSheet('border-radius:10px;color:white;background-color:#00FFFF;font-weight:bold;')

    @pyqtSignature("")
    def on_pushButton_8_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_8.setStyleSheet("border-radius:10px;color:white;background-color:#CC0000;font-weight:bold;")
        str=self.mydata.button_data(u' 停',flag=True)
        self.textBrowser_2.append(str)
        self.textBrowser_2.moveCursor(QTextCursor.End)
        self.dir="S"
        self.sendCarMsg()
        
    @pyqtSignature("")
    def on_pushButton_8_released(self):
        self.pushButton_8.setStyleSheet("border-radius:10px;color:white;background-color:#FF0000;font-weight:bold;")

    @pyqtSignature("")
    def on_pushButton_4_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_4.setStyleSheet('border-radius:10px;color:#DDDDDD;background-color:#44FFFF;font-weight:bold;')
        str=self.mydata.button_data(u' 方向:上')
        self.textBrowser_2.append(str)
        self.textBrowser_2.moveCursor(QTextCursor.End)
        self.dir="U"
        self.sendCarMsg()
        
    @pyqtSignature("")
    def on_pushButton_4_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_4.setStyleSheet('border-radius:10px;color:white;background-color:#00FFFF;font-weight:bold;')

    @pyqtSignature("")
    def on_pushButton_6_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_6.setStyleSheet('border-radius:10px;color:#DDDDDD;background-color:#44FFFF;font-weight:bold;')
        str=self.mydata.button_data(u' 方向:左')
        self.textBrowser_2.append(str)
        self.textBrowser_2.moveCursor(QTextCursor.End)
        self.dir='R'
        self.sendCarMsg()
        
    @pyqtSignature("")
    def on_pushButton_6_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_6.setStyleSheet('border-radius:10px;color:white;background-color:#00FFFF;font-weight:bold;')
    
    @pyqtSignature("")
    def on_pushButton_9_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        reply = QtGui.QMessageBox.question(self, u'关掉BeltaGo?',
        u'你真的真的真的要关掉BeltaGo?', QtGui.QMessageBox.Yes,
        QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            str=self.mydata.button_data(u' 关掉BeltaGo',True)
            self.textBrowser_2.append(str)
            self.textBrowser_2.moveCursor(QTextCursor.End)
            #os.system("shutdown -h 5")
            
    @pyqtSignature("int")
    def on_horizontalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        str=self.mydata.slider_data(value)
        self.textBrowser_2.append(str)
        self.textBrowser_2.moveCursor(QTextCursor.End)
        self.car_speed=value
        self.sendCarMsg()
        
    @pyqtSignature("bool")
    def on_radioButton_clicked(self, checked):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        global audio,record_t
        movie=QMovie(":/icon/icon/siri.gif")
        self.label_4.setMovie(movie)
        
        if checked:
            self.label_4.setStyleSheet("")
            movie.start()
            if self.thread_flag == 0:
                print "abcd"
                self.start_flag=1
                record_t = MyThread(ui.record_wave, (ui,), ui.record_wave.__name__)
                record_t.setDaemon(True)
                record_t.start()
                self.thread_flag=1
        else:
            movie.stop()
            self.label_4.setStyleSheet("border-image: url(:/icon/icon/siri.gif);")
            if self.thread_flag == 1:
                self.start_flag=0
                self.thread_flag=0
    
    @pyqtSignature("")
    def on_horizontalScrollBar_2_sliderReleased(self):

        self.armx=self.horizontalScrollBar_2.value()
        time.sleep(0.1)
        self.sendArmMsg()
    
    
    @pyqtSignature("")
    def on_horizontalScrollBar_3_sliderReleased(self):

        self.army=self.horizontalScrollBar_3.value()
        time.sleep(0.1)
        self.sendArmMsg()
    
    @pyqtSignature("")
    def on_horizontalScrollBar_4_sliderReleased(self):

        self.armz=self.horizontalScrollBar_4.value()
        time.sleep(0.1)
        self.sendArmMsg()
        
    @pyqtSignature("")
    def on_pushButton_10_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pump=1-self.pump
        if self.pump == 1:
            self.pushButton_10.setText(u'on')
        else:
            self.pushButton_10.setText(u'off')
        self.sendArmMsg()
    
    @pyqtSignature("")
    def on_pushButton_11_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_11.setStyleSheet("border-radius:10px;color:#DDDDDD;background-color:#FFFF44;font-weight:bold;\n")
        if not self.armlock:
            self.m=1
            self.sendArmMsg()
        else:
            self.m=0
            QMessageBox.about(self, u'warniing', u'arm is moving')
        
    @pyqtSignature("")
    def on_pushButton_11_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.pushButton_11.setStyleSheet("border-radius:10px;color:white;background-color:#FFFF00;font-weight:bold;\n")



        
if __name__ == "__main__":
    import sys
    sys.getdefaultencoding()
    reload(sys)
    sys.setdefaultencoding('utf8')
    rospy.init_node("BgGui")
    app = QtGui.QApplication(sys.argv)
    ui =MainWindow()
    ui.setDaemon(True)
    ui.start()
    ui.show()
    sys.exit(app.exec_())
    
