import customizableredirector
import socket
SLEEPY_LINER = "zzzZZZzzzZZZzzzZZZzzzZZZ"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80)) 
IP_ADDR = s.getsockname()[0]
s.close() # stolen from so: https://stackoverflow.com/a/166589
del socket # saves miniscule amount of ram
print(SLEEPY_LINER)
print("DREAM REDIRECTOR")
print(SLEEPY_LINER)
print("Set your proxy to:")
print(IP_ADDR + ":8080")
print("Note: Results may be")
print("inaccurate! It should")
print("Start with \"192.168\"")
print(SLEEPY_LINER)
print("Make sure you are on")
print("the same Wi-Fi as your")
print("DS!")
print(SLEEPY_LINER)
customizableredirector.CustomizableRedirector(("0.0.0.0", 8080), redir={"en-ds.pokemongl.com": "127.0.0.1:5000"}).start()