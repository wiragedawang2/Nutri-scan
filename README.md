# backend installation
The backend need import all modul need, follow the steps below for run the backend

install virtual environtment for python
-
Before install the pip create folder virtual for environtment `python -m venv venv`<br>

instal pip needed
-
you need install all pip need
1. `pip install fastapi uvicorn pyzbar Pillow `
2. `pip install request`
3. `pip install opencv-python`
<br>

more information
-
in code line 16 ` allow_origins=["http://127.0.0.1:5500", "localhost"]` you need ajust your frontend host and port for make sure both browser and postman can run corectly<br>
if the backend can olny running well in postman but not in browser, please ajust frontend host and port because it importan to connect between diffrent port 
