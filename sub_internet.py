
'''
import ping, socket
def test():
    try:
        ping.verbose_ping('www.google.com', count=3)
        results = ping.Ping('www.wikipedia.org', timeout=2000).do()

    except socket.error as e:
        print ( "Ping Error:" + e)



#pip install pythonping
from pythonping import ping

def test(tURL):
    #tResults = ping('127.0.0.1', verbose=True)
    tResults = ping(tURL, verbose=True)
    print("********** ping ***************")
    print(tResults)
    print("*******************************")

test("www.google.com")

Operations not permitted.

'''

from urllib import request

def check():
    try:
        #request.urlopen('http://216.58.192.142', timeout=1)
        request.urlopen('https://www.google.com/', timeout=1)
        
        return True
    except request.URLError as err: 
        print("********** Not connected to the Internet ***************")
        return False

#tBool = internet_on()
#print(tBool)