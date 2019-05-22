import xenapi as XenAPI
class Auth:
    
    sx = object

    @staticmethod
    def get_session(xenmaster, username, password):
        url = "https://{}".format(xenmaster)
        session = XenAPI.Session(url, ignore_ssl=True)
        try:
            session.login_with_password(username,password,"1.0","citrix.py")
        except (XenAPI.Failure, e):
            if (e.details[0] == 'HOST_IS_SLAVE'):
                session=XenAPI.Session("https://{}".format(e.details[1]))
                session.login_with_password(username,password)
            else:
                raise
        sx = session.xenapi        
        return sx

    
    @staticmethod
    def close_session():
        sx.logout()


if __name__ == "__main__":
    print("Open session\n")
    Auth.get_session("africa", "root", "t1hu4n4123")
    print("Close session\n")
    Auth.close_session()