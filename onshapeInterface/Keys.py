
class Keys:
    def __init__(self, accessKey, secretKey):
        self.secretKey = secretKey
        self.accessKey = accessKey

    def getAccessKey(self):
        return self.accessKey

    def getSecretKey(self):
        return self.secretKey