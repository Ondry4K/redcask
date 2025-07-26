# RedCask  
A simple solution to a probably non-existent problem.
## Notice:  
I know there's a million ways to do this but better, I've only made this as a proof of concept.

## Server Instructions
1. Download the latest release as zip from https://github.com/Ondry4K/redcask/releases/
2. Unzip the archive in a place where you want RedCask to live  
   *optional but recommended: set up a virtual enviroment with python, see: https://docs.python.org/3/library/venv.html
3. Install all dependencies via pip:
  ```python
pip install fastapi csv pydantic pathlib uuid datetime base64 dotenv
```
5. Set up the .env in the root (basically: create a file named .env)
  In this file it will include one entry named "KEY" (all uppercase, it's case sensitive) and a value with the key you want to use.  
  eg.
```env
KEY=TOP_SECRET
```  
  In this step I also suggest encoding your key in base64 and saving it to a txt folder somewhere for later use because you will need it.  
7. Test the app with fastapi:  
   ```python
   fastapi dev server.py --host 0.0.0.0 --port 8000 --reload
   ```  
   (p.s.: you can change the port to whatever your heart desires)
8. If you set up everything correctly you should be able to access the server on the localhost, the root contains the web ui.  
  ## IF something went wrong:
  - either i fucked up (very likely)
  - you fucked up
## part dos: Client Instructions
This is the part where you die.. wait no.. wrong reference.  
This part is where the other devices you want to download the torrents to come into play, download the latest release https://github.com/Ondry4K/redcask/releases/  
If you wanna be tidy and use arch linux and cannot deal with messy directories; first of all, fuck you. Now to the point, you can delete everything **BUT** the "client" directory
1. Install dependencies with pip:  
   ```python
   pip install colorama requests libtorrent dotenv logging base64 uuid json
   ```
   (i will commit war crimes if i forgot a dependency)
3. Set up the .env file (create a file named ".env" and input this inside:
   ```env
   server_key=TOP_SECRET # REPLACE WITH ACTUAL SERVER_KEY
   server_ip=127.0.0.1 # REPLACE WITH ACTUAL SERVER IP
   port=8000 # (optional) if you have a different port, input it here, else just leave default
   save_path="./" # change to the save path you want your torrents to be downloaded to```
4. fhUUUUCK the conf.json file that we (yes we) are too lazy to use to actually save configuration (by this im trying to say you dont need the file you pure soul)
5. Run the python file:  
   ```python
   python client.py
   ```  
   It's gonna, (you won't believe this) **AUTOMATICALLY** log in to the server using the API and start searching for torrents to download like a feral rat on steroids,  
   and it's not stopping anytime soon. This is why I suggest you set up the server first.
## part tres: web-ui instructions for challenged ones
1. make sure your server is running (aka finish the server instructions before you come here)
2. visit your server's ip by default on port 8000 (so that means "123.456.789.000:8000")
3. it should spit you out to a login page, you will enter the **BASE64 ENCODED SERVER KEY YOU SET UP IN .ENV**
4. finito, you are now logged in and ready to rumble, add torrents with a proper device ID and it will start downloading automatically if there are any online clients with that UUID

## suggestion:
if you like my sub-par intelligence explaining you should give this repo a star
