from flask import Flask
from blueprint.comment import comment
from blueprint.main_page import main_page
from blueprint.detail_page import detail_page

app = Flask(__name__)
app.register_blueprint(comment.comment)
app.register_blueprint(main_page.main_page)
app.register_blueprint(detail_page.detail_page)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True, port=80)
