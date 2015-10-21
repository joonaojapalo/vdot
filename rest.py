from urlparse import urlparse

from twisted.web import server, resource
from twisted.internet import reactor, endpoints


def vdot(path, query):
	return "I am request #%i\n" % self.numberRequests


class Router(resource.Resource):
    isLeaf = True
    numberRequests = 0
    
    def __init__(self, routes):
    	resource.Resource.__init__(self)
    	self.routes = routes

    def render_GET(self, request):
    	uri = urlparse(request.uri)
    	print uri.path
        self.numberRequests += 1
        request.setHeader("Content-type", "text/plain")
        return self.routes[uri.path]


routes = {
	"/vdot": vdot
}

endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(Router(routes)))
print "starting..."
reactor.run()

print "done"
