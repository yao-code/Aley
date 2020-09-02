class MyResponse(object):
    def __init__(self, code=200, msg="OK", data=None):
        self.code = code
        self.msg = msg
        self.data = data
    
    def to_dict(self):
        return self.__dict__

    def error_response(self, msg):
        self.code = 400
        self.msg = msg
        return self.__dict__