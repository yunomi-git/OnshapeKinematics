class APICallCreator:
    def __init__(self, documentID, workspaceID, elementID):
        self.documentID = documentID
        self.workspaceID = workspaceID
        self.elementID = elementID
        self.category = "partstudios"

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

