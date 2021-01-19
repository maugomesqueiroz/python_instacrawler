class LoginError(Exception):
    """Exception raised if login information causes alert message in instagram
    login page.

    Attributes:
        alert_message -- input alert message which caused the error
    """

    def __init__(self, alert_message, message="Login Error: "):
        self.alert_message = alert_message
        self.message = message + alert_message
        super().__init__(self.message)
