# pastecat
Server Side Script For Using `nc` To Paste The Output On A Pastebin

Use `git clone https://github.com/beepaste/pastecat.git && cd pastecat`

Then run `python pastecat.py`

# installation
just clone this repo on your server, then copy the `pastecat.py` to `/usr/bin/` and `pastecat` to `/etc/init.d/` (for init systems) or `pastecat.service` to `/etc/systemd/system/` (for systemd systems).
Don't forget to check if both files are executable, and the settings on the `pastecat.py` are ok!

#Usage:
you need `netcat` installed inorder to send the output to pastebin.

Pipe Your Command to `nc host 1111` To Send The Output

NOTE: You can use pastecat without nc using the following alias:

Bash:

`alias bp="(exec 3<>/dev/tcp/ncbeepaste.io/1111; cat >&3; cat <&3; exec 3<&-)"`

Fish:

alias bp=

usage:

`echo this is a test! | bp`


#Example:

`uname -a | nc nc.beepaste.io 1111`
