# **remote-file-storage**
like the name suggest, this is a remote file storage 

## **Features:**
- remove files
- edit file/folder/directory 's name
- download files
- upload files
- make folder/directory
- view files(only pictures, videos, sounds, pdf, html, or anything that your broswer supports)
- trash bin recovery
- local network access(or world-wide with tunneling)
- authentication before accessing the files
- cool asset art

## **Requirements:**
- python — (3.12+)
- library:
  - flask — (`python -m pip install flask` or in mac/linux `python3 -m pip install flask`)
  - window:
    - waitress — (`pip install waitress`)
  - MacOs/linux:  
    - gunicorn — (`python -m pip install gunicorn` or in mac/linux `python3 -m pip install gunicorn`)

# **WAIT!**
before doing anything make sure to edit the auth key in the main.py to make sure that no one can access to the file storage except you and trusted people

## **Run:**
- Window:
  - `python -m waitress --host=0.0.0.0 --port=80 --threads=4 main:app`
  - make sure you run cmd as administrator
- MacOs:
  - uhhhhh i've never used macos before but i'm guessing `sudo python3 -m gunicorn -w 4 -b 0.0.0.0:80 main:app --timeout 1800`
- linux:
  - `sudo python3 -m gunicorn -w 4 -b 0.0.0.0:80 main:app --timeout 1800`

## **how do i access it?**
- window:
  - type `ipconfig` into cmd
  - find "`IPv4 Address. . . . . . . . . . . :`"
  - go to your broswer then enter the ip that you saw
  - enter your auth token
  - done! have fun!
- macos:
  - idk lol gl finding your local ip
- linux:
  - type `ip a` into your terminal
  - look for the line starting with "`inet`"
  - look for 4 number that has `.` inbetween
  - that's your local ip
  - enter that into your broswer
  - enter your auth token
  - done! havee fun!
