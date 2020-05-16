from src.main import *
import pytest

@pytest.fixture
def api():
    return ultra()

@pytest.fixture
def client(api):
    return api.test_session()

def test_basic_route(api):
    @api.route("/")
    def index():
        return "Hi Bois!"

def test_dynamic_route(api, client):
    @api.route("/isbn/<isbn>")
    def books(isbn):
        return f"Book Isbn: {isbn}"

    assert client.get("http://localhost:8000/isbn/9849765478").text == "Book Isbn: 9849765478", "Dynamic Route Not Working!"
    
def test_post(api, client):
    @api.route("/login")
    def login():
        if request.data['username'] == "hi" and request.data['password'] == "bois":
            return "You're In!"
        else:
            return "OOF"

    assert client.post("http://localhost:8000/login", data={'username': 'hi', 'password': 'bois'}).text != "OOF", "Post data get not working!"

def test_page_not_found(api, client):
    assert client.get("http://localhost:8000/page_not_found").text == """<h1 style="text-align: center; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">404 Page Not Found</h1>""", "404 isn't working!"