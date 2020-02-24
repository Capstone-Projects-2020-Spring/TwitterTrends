
# TODO: Add data classes and data structures to this file
# Ex: Tweets class. User class


# [User class]
class User:

    def __init__(self, uid, uname, uemail):
        self.userId = uid
        self.userName = uname
        self.userEmail = uemail

    def get_id(self):
        return self.userId

    def set_id(self, uid):
        self.userId = uid

    def get_username(self):
        return self.userName

    def set_username(self, uname):
        self.userName = uname

    def get_email(self):
        return self.userEmail

    def set_email(self, uemail):
        self.userEmail = uemail
# end User class


class Tweet:

    def __init__(self, uid, userid, postid, body):
        self.tweetId = uid
        self.userId = userid
        self.postId = postid
        self.content = body

    def get_id(self):
        return self.tweetId

    def set_id(self, uid):
        self.tweetId = uid

    def get_userId(self):
        return self.userId

    def set_userId(self, uid):
        self.userId = uid

    def get_postId(self):
        return self.postId

    def set_postId(self, pid):
        self.postId = pid

    def get_content(self):
        return self.content

    def set_content(self, body):
        self.content = body