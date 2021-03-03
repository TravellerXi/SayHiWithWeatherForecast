#!/usr/bin/env python3
# coding:utf-8
# need to: pip install qcloudsms-py

import urllib3
import sys
import datetime
from qcloudsms_py import SmsSingleSender

class WeatherForecastSender():
    def __init__(self,CityCode):
        """
        :param CityCode: 城市或者县的拼音，如杭州市:hangzhou 下城区:xiachengqu, string type
        如何测试你填的CityCode是否正确呢?试试在浏览器里能否打开 http://www.tianqi.com/ + CityCode
        :return:
        """
        try:
            http = urllib3.PoolManager()
            sysEncode = sys.getfilesystemencoding()
            url = 'http://www.tianqi.com/' + CityCode
            RawData = http.request("GET", url)
            RawData = RawData.data.decode(sysEncode)
            RawData = RawData[int(RawData.find('class="weather"')):int(RawData.find('class="day7"'))]
            self.Temperature = RawData[
                               (int(RawData.find('<p class="now"><b>')) + 18):int(RawData.find('</b><i>℃</i></p>'))]
            RawData = RawData[(int(RawData.find('<span><b>')) + 9):]
            self.Weather = RawData[:int(RawData.find('</b>'))]
            self.TemperatureRange = RawData[6:int(RawData.find('</span>'))]
            RawData = RawData[(int(RawData.find('湿度：')) + 3):]
            self.Humidity = RawData[:RawData.find('</b>')]
            RawData = RawData[int(RawData.find('风向：')):]
            self.WindDirection = RawData[3:][:RawData.find('</b>') - 3]
            RawData = RawData[(int(RawData.find('紫外线：')) + 3):]
            self.Ultravioletrays = RawData[1:RawData.find('</b>')]
            RawData = RawData[int(RawData.find('空气质量：')) + 5:]
            self.AirQuality = RawData[:int(RawData.find('</h5>'))]
            RawData = RawData[int(RawData.find('日出:')) + 3:]
            self.Sunrise = RawData[:int(RawData.find('<br'))]
            RawData = RawData[int(RawData.find('日落:')) + 3:]
            self.Sunset = RawData[:int(RawData.find('</span>'))]
            print(self.Weather, self.AirQuality, self.Sunset, self.WindDirection, self.Humidity, self.Ultravioletrays,
                  self.Temperature, self.Sunrise, self.TemperatureRange)

            Blank = " "
            if self.Weather.find('雨') > 0:
                self.Weather_Msg = "  雨天记得带伞哦。"
            else:
                self.Weather_Msg = Blank
            self.HighTemperature = int(
                self.TemperatureRange[(int(self.TemperatureRange.find('~')) + 1):int(self.TemperatureRange.find('℃'))])
            if self.HighTemperature > 30:
                self.TemperatureRang_Msg = " 仙女也要注意防晒哦。"
            else:
                self.TemperatureRang_Msg = Blank
            if self.Ultravioletrays.find("强") > 0:
                self.Ultravioletrays_Msg = " 带上防晒霜哈"
            else:
                self.Ultravioletrays_Msg = Blank
            if self.AirQuality.find("污染") > 0:
                self.AirQuality_Msg = " 污染严重，记得戴口罩哈"
            else:
                self.AirQuality_Msg = Blank
        except:
            print("failed to init, try again later or check the website")
    def SendWeatherReportByMsg(self,Nickname,CityChinese,PhoneNumber,appid,appkey,template_id):
        """
        调用腾讯云短信API，发送短信提示，需要事先在腾讯云里申请短信模板。
        :param Nickname: 可可爱爱的昵称，如小仙女, string type
        :param CityChinese:城市中文名，如北京, string type
        :param PhoneNumber:手机号, string type
        :return:
        """
        thisYear = str(datetime.datetime.now().year)
        thisMonth = str(datetime.datetime.now().month)
        thisDay = str(datetime.datetime.now().day)
        params = [Nickname, thisYear, thisMonth, thisDay, CityChinese, self.Weather, self.Weather_Msg, self.HighTemperature, self.Temperature,\
                  self.Ultravioletrays_Msg, self.WindDirection, self.Ultravioletrays, self.Ultravioletrays_Msg, self.AirQuality,self.AirQuality_Msg,\
                  self.Sunrise,self.Sunset]
        ssender = SmsSingleSender(appid, appkey)
        try:
            ssender.send_with_param(86, PhoneNumber,
                                             template_id, params)
        except Exception as e:
            print(e)




if __name__=="__main__":
    ######################################
    # 此区域填入腾讯云短信API接口信息
    appid = 0
    appkey = ""
    template_id = 0
    ######################################
    thisWeather=WeatherForecastSender("xuhuiqu")
    thisWeather.SendWeatherReportByMsg("小仙女","徐汇区","18888888888")