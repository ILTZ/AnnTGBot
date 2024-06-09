
class DBHandler:

    def __init__(self):         
        pass

    def AddNewUser(self, login, description, birthday, rContent, startPictureSlots):                
        pass

    def AddNewPicture(self, userID, description, picture, rContetMark):
        pass

    def AddUserLink(self, userID, link):
        pass

    def AddPictureReview(self, reviewerID, pictureID, text, rating):
        pass

    def GetUserPictures(self, userID, rContent):
        pass

    def GetUserLinks(self, userID):
        pass

    def GetUserInfo(self, tgLogin):
        pass

    def GetPictureReview(self, pictureID):
        pass

