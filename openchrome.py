import webbrowser as wb
import platform 

plt = platform.system()

def webauto():
    if plt == "Windows":
      chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    elif plt == "Linux":
      chrome_path = '/usr/bin/google-chrome'
    elif plt == "Darwin":
      print("Your system is MacOS, Gross!")
    URLS = ("gmail.com", "github.com/hansendm", 
            "https://discord.gg/4dUquty", "stackoverflow.com","youtube.com")

    for url in URLS:
        print("Opening: " + url)
        wb.get(chrome_path).open(url)

webauto()
  
