# -*- coding: utf-8 -*-

import wave
from pyaudio import PyAudio, paInt16
import urllib2, urllib, pycurl
import json
import threading
import Queue
from time import sleep, ctime
from StringIO import StringIO
import numpy as np


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def gerResult(self):
        return self.res

    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.func, self.args)
        print self.name, 'finished it:', ctime()


class myAudio(threading.Thread):
    def __init__(self):
        self.framerate = 8000
        self.NUM_SAMPLES = 2000
        self.channels = 1
        self.sampwidth = 2
        self.TIME = 2
        self.file_name_index = 1
        self.wav_queue = Queue.Queue(1024)
        self.LEVEL = 400
        self.mute_begin = 0
        self.mute_count_limit = 50
        self.mute_end = 1
        self.not_mute = 0
        self.voice_queue = Queue.Queue(1024)
        self.thread_flag = 0
        self.start_flag = 1
        threading.Thread.__init__(self)

    def save_wave_file(self, filename, data):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes("".join(data))
        wf.close()

    def run(self):
        print 'starting', self.name, 'at:', ctime()
        self.res = apply(self.my_record())
        print self.name, 'finished it:', ctime()

    def writeQ(self, queue, data):
        queue.put(data, 1)

    def readQ(self, queue):
        val = queue.get(1)
        return val

    def my_record(self):
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
            # my_buf.append(string_audio_data)
            # count+=1
            # print '.'
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

    def get_token(self):
        apiKey = "h2fAPxonRVm8e59GMojhpEH8"
        secretKey = "d55e1e38ea4932e78bf4abac3def1401"
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey
        res = urllib2.urlopen(auth_url)
        json_data = res.read()
        print 'json_data:', type(json_data)
        return json.loads(json_data)['access_token']

    def dump_res(self, buf):
        print buf
        my_temp = json.loads(buf)
        if my_temp['err_no']:
            if my_temp['err_no'] == 3300:
                print u'参数输入不正确'
            elif my_temp['err_no'] == 3301:
                print u'识别错误'
            elif my_temp['err_no'] == 3302:
                print u'验证失败'
            elif my_temp['err_no'] == 3303:
                print u'语音服务后端问题'
            elif my_temp['err_no'] == 3304:
                print u'请求GPS过大，超过限额'
            elif my_temp['err_no'] == 3305:
                print u'产品线当前日请求数超过限额'
        else:
            my_list = my_temp['result']
            print type(my_list)
            print my_list[0]

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
            # c.setopt(c.RETURNTRANSFER,1)
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
            sleep(0.3)


if __name__ == '__main__':
    audio = myAudio()
    audio.setDaemon(True)
    audio.start()
    print 'over'
    audio.thread_flag = 1
    audio.start_flag = 1
    record_t = MyThread(audio.use_cloud, (audio.get_token(),), audio.use_cloud.__name__)
    record_t.setDaemon(True)
    record_t.start()
    audio.use_cloud(audio.get_token())
    print 'OK!'