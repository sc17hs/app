import requests
import json


token = None



def register():
    print("This is the register function")
    username = str(input("Username: "))
    email = str(input("Email: "))
    password = str(input("Password: "))
    data = {"username": username,
            "email": email,
            "password": password}
    r = requests.post("http://127.0.0.1:8000/register/", data = data )
    #print(r.text)
    if "already exists" in r.text:
        print("That user already exists try again or log in")
        register()
    #print(data)


def login(url):
    url = url
    url = "http://127.0.0.1:8000/login/"
    print("This is the login function")
    username = str(input("Username: "))
    password = str(input("Password: "))
    data = {'username': username,
            'password':password}
    r =requests.post(url, data = json.dumps(data))
    if "token" in r.text:
        #print("Token Returned ")
        print("Login successful")
        return r.text
    else:
        print(r.text)
        print("Please Try again")
        login(url)


def list():
    print("This is the list function")
    r = requests.get("http://127.0.0.1:8000/modules/")
    #print(r.text)
    response = json.loads(r.text)
    for x in response:
        teacher = ''
        for z in x['teachers']:
            teacher = teacher + ',' + str(z['name']) + '-' + str(z['code'])
        print(x['code']+'-'+str(x['name'])+'-'+str(x['year'])+'-'+str(x['semester'])+'-'+str(teacher))


def view():
    print("This is the view function")
    r = requests.get("http://127.0.0.1:8000/professors/")
    response = json.loads(r.text)

    for x in response:
        print('The rating of '+str(x['name'])+'('+str(x['code'])+')'+' is '+ str(x['rating']))


def average(professor_id,module_code):
    print("This is the average function")
    professorid = professor_id
    modulecode = module_code
    r = requests.get("http://127.0.0.1:8000/average/"+professorid+'/'+modulecode+'/')
    response = json.loads(r.text)
    response = response[0]
    print("The rating of "+response['name']+'('+response['code']+')'+' in module '+module_code+' is '+response['rating'])


def rate(token,professor_id,module_code,year,semester,rating):
    if token==None:
        print("You must be logged in to rate ")
        return
    else:
        professorid = professor_id
        module_code = module_code
        year = int(year)
        semester = int(semester)
        rating = int(rating)
        data = {
                'professorid': professorid,
                'module_code':module_code,
                'year': year,
                'rating': rating}
        headers = {
            'Authorization': token
        }
        r = requests.post("http://127.0.0.1:8000/rating/",  headers= headers ,data = json.dumps(data))
    print("Rating Added")
























def Menu():
    print('-'*50)
    print('1.register \n2.login <url> \n3.logout\n4.list\n5.view\n6.average <professorid> <modulecode>\n7.rate < professor_id> <module_code> <year> <semester> <rating>\n8.quit\n')
    option = str(input(":- "))
    global token
    if option.startswith('register'):
        register()
        print("Registered successfully")
    if option.startswith('login'):
        url = option[6::]
        token = login(url)
        token = str(token[10:-2])
        token = 'token '+token
        #print(token)
    if option.startswith('logout'):
        token = None
        print("Logged out")
    if option.startswith('list'):
        list()
    if option.startswith('view'):
        view()
    if option.startswith('average'):
        professor_id = option[8:-4]
        module_code = option[12:]
        average(professor_id,module_code)
    if option.startswith('rate'):
        professor_id = option[5:-13]
        module_code = option[9:-9]
        year = option[13:-4]
        semester = option[18:-2]
        rating = option[20:]
        rate(token,professor_id,module_code,year,semester,rating)
    if option.startswith('quit'):
        quit()
    Menu()

Menu()
