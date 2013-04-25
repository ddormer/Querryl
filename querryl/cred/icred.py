from twisted.cred.credentials import ICredentials

class ISessionCredentials(ICredentials):
    """
    Cookie-based session credentials.
    """
    def checkUsername():
        """
        Return C{self.username}.
        """
