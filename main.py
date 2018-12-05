from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
import json

import urllib2
import re
import time

GET_IP_COUNT = 4

def debug(str, obj = None):
   print("[%s]%s" % (time.strftime(' %Y-%m-%d %H:%M:%S',time.localtime(time.time())), str))
   if (obj != None):
      print(obj)

def GetIP(method):
   if method == 0:
      url = "http://checkip.dyndns.org"
      request = urllib2.urlopen(url).read()
      theIP = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}",request)
      return theIP[0]
   elif method == 1:
      return urllib2.urlopen('http://ip.42.pl/raw').read()
   elif method == 2:
      return json.load(urllib2.urlopen('http://jsonip.com'))['ip']
   elif method == 3:
      return json.load(urllib2.urlopen('http://httpbin.org/ip'))['origin']

def ReplaceIP(ip):
	#域名名字
	domainName = "***"

	#阿里云域名后台的信息
   client = AcsClient(
      "***",
      "***",
      "***"
   );

   request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
   request.set_DomainName(domainName)
   request.set_RRKeyWord("www")

   response = client.do_action_with_exception(request)
   debug("query list:", response)
   json_value = json.loads(response)
   RecordID = json_value["DomainRecords"]["Record"][0]["RecordId"]

   if (json_value["DomainRecords"]["Record"][0]["Value"] == ip):
      debug("web ip is some." + ip)
      return
   else:
      debug("pre ip:" + json_value["DomainRecords"]["Record"][0]["Value"])
      debug("now ip:" + ip)

   request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
   request.set_RecordId(RecordID)
   request.set_RR("www")
   request.set_Type("A")
   request.set_Value(ip)

   response = client.do_action_with_exception(request)
   debug("update result:", response)

def Run():
   IP = ""
   getIpMethod = 0
   while (True):
      try:
         ip = GetIP(getIpMethod)
         if (ip != IP):
            IP = ip
            ReplaceIP(IP)
         else:
            debug("ip is some." + ip)
         time.sleep(10 * 60)
      except BaseException, e:
         debug("happen error:", e)
         time.sleep(10)
         getIpMethod = (getIpMethod + 1) % GET_IP_COUNT

if __name__ == '__main__':
   Run()