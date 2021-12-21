from App import create_app
from App.constant import TITLE

app = create_app()

if __name__ == "__main__":
    app.run()