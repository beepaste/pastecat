#!/bin/bash
echo 'Installation of Pastecat is now started, before we continue please configure port number in src/pastecat.py';
echo 'Press any key to continue...';
read key;

if [[ -f /etc/redhat-release ]]; then

echo 'Installing Pastecat For RedHat Release: \n';

elif [[ -f /etc/debian_version ]]; then

    echo 'Installing Pastecat For Debian Release: \n';
else
    echo 'Installing Pastecat For Other Operating System';
fi

MASTER=$(sudo su -c 'stat /proc/1/exe | head -1 | awk "{print $NF}" | rev | cut -d "/" -f 1 | rev');

# if [[ $? -eq 1 ]]; then
#     clear;
#     echo 'Installation Failed, Permission Denied.';
#     exit;
# fi
if [[ $MASTER == 'systemd' ]]; then

    echo 'Configuring Service';
    sudo su -c 'cp src/pastecat.service /etc/systemd/system/; chmod +x /etc/systemd/system/pastecat.service';

elif [[ $MASTER == 'init' ]]; then

    echo 'Configuring Service';
    sudo su -c 'cp src/pastecat /etc/init.d/; chmod +x /etc/init.d/pastecat';

elif [[$MASTER != 'systemd' && $MASTER != 'init']]; then
    echo 'Can not install Pastecat on this OS, follow instructions from developers.';
    exit;
fi

echo 'Installing Sources.'
sudo su -c  'cp src/pastecat.py /usr/bin/; chmod +x /usr/bin/pastecat.py';

echo 'Installation is now done, do you want to add a shortcut to use? e.g. "cat file.txt | bp" ';
echo '[y/n/yes/no]:';
read des;

if [[ $des == 'y' || $des == 'yes' ]]; then
    echo 'Creating shortcut, please tell us which port do you use for pastecat: ';
    read port;
    user_shell=$(echo $SHELL | rev | cut -d "/" -f1 | rev);
    if [[ $user_shell == 'bash' ]]; then
        echo 'alias bp="(exec 3<>/dev/tcp/nc.beepaste.io/1111; cat >&3; cat <&3; exec 3<&-)"' >> ~/.bashrc;
        echo 'Installation Done.';
        exit;
    elif [[ $user_shell == 'zsh' ]]; then
        echo 'alias bp="(exec 3<>/dev/tcp/nc.beepaste.io/1111; cat >&3; cat <&3; exec 3<&-)"' >> ~/.zshrc;
        echo 'Installation Done.';
        exit;
    else
        echo 'Sorry, you are using unsupported shell, pleade do alias bp="(exec 3<>/dev/tcp/nc.beepaste.io/1111; cat >&3; cat <&3; exec 3<&-)"';
        echo 'Installation will now exit.';
        exit;
    fi
fi
echo 'Installation Done.';
exit;
