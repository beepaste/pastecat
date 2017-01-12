# pastecat
Server Side Script For Using `nc` To Paste The Output On A Pastebin

Use `git clone https://github.com/beepaste/pastecat.git && cd pastecat`

Then run `python pastecat.py`

# installation
just clone this repo on your server, then copy the `pastecat.py` to `/usr/bin/` and `pastecat` to `/etc/init.d`.
Don't forget to check if both files are executable, and the settings on the `pastecat.py` are ok!

#Usage:
you need `netcat` installed inorder to send the output to pastebin.

Pipe Your Command to `nc host 99` To Send The Output

#Example:

`uname -a | nc localhost 99`
