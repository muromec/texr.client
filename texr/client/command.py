from app import app
import handlers
import user_handlers
import os

def main():
    username = os.getenv("TEXR_USER")
    if username is None:
        username = os.getenv("USER")

    if username is None:
        print "Dont know who I am, can't start!"
        return

    app.me(username)
    app.run()

if __name__ == '__main__':
    main()
