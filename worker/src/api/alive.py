import falcon


class Alive(object):


    def __init__(self):
        self.ok = '{ "status": "ok", "response": '
        self.failed = '{"status": "failed", "response": '
        self.tail = '}'

    def on_get(self,req,resp):
        resp.body = (self.ok+'"I\'m alive"'+self.tail)
        resp.status = falcon.HTTP_200
