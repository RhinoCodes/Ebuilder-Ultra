from src.main import ultra, request

app = ultra()
@app.route("/")
class index:
    def get(self):
        return "HI GUYS!"
        
    def post(self):
        return "Now class, NO HACKING! Oh yeah, Jimmy, here's your variables: "+str(request.data)

@app.route("/login")
def login():
    if request.data['username'] == "hi" and request.data['password'] == "bois":
        return "You're In!"
    else:
        return "OOF"

app.run()