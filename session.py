
import pickle



"""
    User oriented object
    For each user we create new session

    FINITE STATE MACHINE CONCEPT!
"""
class Session:
    def __init__(self, sesionID, username):
        self.sesionID = sesionID
        self.username = username
        self.fsm_state = None


"""
    All sessions are managed by session manager object
    
    TODO - add errorrs processing
    
    TODO - add hashing to passwords
"""
class SessionManager:
    def __init__(self):
        self.sessionMap = {}
        self.usersDatabase = {}
        with open('auth.pkl', 'rb') as f:
            self.usersDatabase = pickle.load(f)


    def __auth__(self, username, password):
        if ((username in self.usersDatabase) and (self.usersDatabase[username] == password)):
            return True
        else:
            return False

    """
        Here we checking user logging in details
        and creating new session in case of success
        
        TODO - add hashing (in case of safety)
    """
    def addSession(self, sessionID, username, password):
        if (sessionID not in self.sessionMap.keys()):
            authResult = self.__auth__(username, password)
            if authResult:
                self.sessionMap[sessionID] = Session(sessionID, username)
                return True
            else:
                return False
        else:
            return "already"


    def addUserAdmined(self, username, password):
        self.usersDatabase[username] = password
        with open('auth.pkl', 'wb') as f:
            pickle.dump(self.usersDatabase, f)

    """
        In ideal approach we should set some Time To Live for each session
    """
    def removeSession(self, sessionID):
        if sessionID in self.sessionMap:
            del self.sessionMap[sessionID]


    def isAuthorized(self, sessionID):
        if (sessionID in self.sessionMap):
            return True
        else:
            return False

    def isNotAuthorized(self, sessionID):
        if (sessionID in self.sessionMap):
            return False
        else:
            return True

    def isAdminAuth(self, sesionID):
        if ((sesionID in self.sessionMap) and self.sessionMap[sesionID].username == "admin"):
            return True
        else:
            return False


    def getUserName(self, sessionID):
        return self.sessionMap[sessionID].username

    def isUserExist(self, username):
        if (username in self.usersDatabase.keys()):
            return True
        else:
            return False

    def set_session_state(self, sessionID, state):
        self.sessionMap[sessionID].fsm_state = state

    def get_session_state(self, sessionID):
        return self.sessionMap[sessionID].fsm_state 

