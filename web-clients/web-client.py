from twisted.internet import defer
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from zope.interface import implements, implementer
from twisted.web.client import getPage, downloadPage
from twisted.internet.protocol import Protocol
from twisted.web.http_headers import Headers
import time
import sys



class Enterprise(Protocol):
    def __init__(self, finished):
        self.finished = finished
    def dataReceived(self, data):
        print(data)
    def connectionLost(self, reson):
        self.finished.callback(None)


@implementer(IBodyProducer)
class StringProducer(object):
    ''' 封装body , 为request提供body内容 '''
    def __init__(self, body):
        self.body = body
        self.length = len(body)
    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)
    def pauseProducing(self):
        pass
    def stopProducing(self):
        pass


def printHeaders(response):
    '''打印response信息'''
    print('HTTP version:',response.version)
    print('Status code:', response.code)
    print('Status phrase:', response.phrase)
    print('Response headers:')
    for header,value in response.headers.getAllRawHeaders():
        print(header,value)


def printResource(response):
    finished = defer.Deferred()

    '''Register an IProtocol provider to receive the response body.'''
    response.deliverBody(Enterprise(finished))
    return finished


def printError(failure):
    print(failure)
    
def stop(result):
    reactor.stop()

agent = Agent(reactor)
headers = Headers({
    'User-Agent': [''],
    'Content-Type': ['text/x-greeting']
    })

url = b'http://127.0.0.1:8000'
body = StringProducer(b'http://www.baidu.com')

for i in range(1):
    print(i, url)
    # d = agent.request(b'GET',url)  # 得到一个response
    d = agent.request(b'POST',url, bodyProducer=body)
    d.addCallbacks(printResource, printError)  # printResource(response)

d.addBoth(stop)

reactor.run()

