# This creates the URL request to send to the API, excluding the payload
# Use setRequest() and setCategory() based on the Glassworkd API (google)
class RequestUrlCreator:
    # def __init__(self, documentID, workspaceID, elementID):
    #     self.documentID = documentID
    #     self.workspaceID = workspaceID
    #     self.elementID = elementID
    #     self.category = "partstudios"

    def __init__(self, url):
        self.parseStudioURL(url)
        self.category = "partstudios"
    def parseStudioURL(self, url):
        index = url.find("document")
        index += 1
        closingIndex = url.find("/", index);
        index = closingIndex + 1
        closingIndex = url.find("/", index);
        self.documentID = url[index : closingIndex]

        index = url.find("w/")
        index += 1
        closingIndex = url.find("/", index);
        index = closingIndex + 1
        closingIndex = url.find("/", index);
        self.workspaceID = url[index:closingIndex]

        index = url.find("e/")
        index += 1
        closingIndex = url.find("/", index);
        index = closingIndex + 1
        self.elementID = url[index:]

    def setRequest(self, request):
        self.request = request

    def setCategory(self, category):
        self.category = category
    
    def getURL(self, includeWorkspace=True):
        s = "https://cad.onshape.com/api/"
        s += self.category
        s += "/d/" + self.documentID
        if includeWorkspace:
            s += "/w/" + self.workspaceID
        s += "/e/" + self.elementID
        s += "/" + self.request
        return s

