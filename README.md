# How to setup Video Web Server
1.Disconnect with TELUS VPN

2.Open CMD and run as administrator

3.Change to the location where you want to clone the repository

4.Run command: git clone https://github.com/luchoagomezt/video-web-server.git

5.Run command: cd video-web-server

6.Run command: python -m venv ./venv

Troubleshooting: If "python" is not recognized, check PY_HOME and PATH variable. Python3.7 will work

7.Run command: pip install -r requirements.txt

8.Run command: python ./server.py

9.Open browser and go to https://127.0.0.1:5000 

# How to reconnect to Video Web Server
1.Open CMD and run as administrator

2.Change to the location where you store the repository

3.Run command: venv\scripts\activate

4.Run command: python ./server.py

5.Open browser and go to https://127.0.0.1:5000 
