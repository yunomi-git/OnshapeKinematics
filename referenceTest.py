class Caller:
    def foo(self, input):
        print(input)

class Wrapper:
    def __init__(self, thingToCall):
        self.thingToCall = thingToCall

    def doIt(self):
        self.thingToCall("hello")

caller = Caller()
wrapper = Wrapper(caller.foo)
wrapper.doIt()