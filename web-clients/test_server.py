from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site


class TestPage(Resource):
    '''提供测试服务器: 将客服的Post过来的数据反转后返回'''
    isLeaf = True
    def render_POST(self, request):
        return request.content.read()[::-1]

resource = TestPage()
factory = Site(resource)
reactor.listenTCP(8000,factory)
reactor.run()
