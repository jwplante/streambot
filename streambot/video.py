
class Video:

    def __init__(self, video_name, url, id):
        self.video_name = video_name # Video title
        self.url = url # Url of the video
        self.id = id # UID of the video
        # Dictionary for key-value store with usernames as the key and 
        # "U" - upvote
        # "D" - downvote
        # "N" - no vote
        self.__votes__ = {} 

    def __eq__(self, value):
        return self.video_name == value.video_name and self.url == value.url and self.id == value.id

    def __lt__(self, value):
        return value.num_votes() < self.num_votes()

    def __str__(self):
        return "{}, Link: {}".format(self.video_name, self.url)
    

    def print_with_votes(self):
        return "ID: {}, Votes: {} Title: {}, Link: {}".format(self.id, self.num_votes(), self.video_name, self.url)

    """
    Strips the ID of the YouTube video. Returns empty string if not found.
    """
    def get_video_id(self):
        if (self.url.startswith("https://www.youtube.com/watch?v=")):
            return self.url[32:]
        else:
            return ""


    """
    Get the total value of votes. An upvote is 1 and a downvote is -1
    """
    def num_votes(self):
        total_votes = 0
        for vote in self.__votes__.values():
            if vote == 'U':
                total_votes += 1
            elif vote == 'D':
                if (total_votes > 0):
                    total_votes -= 1
                else:
                    total_votes = 0
        return total_votes
    
    """
    Determine if a person has already voted
    """
    def already_voted(self, user_name):
        return user_name in self.__votes__.keys()


    """
    Upvotes the video from a particular user
    """ 
    def upvote(self, user_name):
        self.__votes__[user_name] = "U"

    
    """
    Downvotes the video from a particular user
    """
    def downvote(self, user_name):
        self.__votes__[user_name] = "D"
    

    """
    Removes the vote from a particular user
    """
    def remove_vote(self, user_name):
        self.__votes__[user_name] = "N"