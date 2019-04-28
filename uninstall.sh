echo BlumeRun UnInstaller
echo ----------------------------------------
echo "Removing Service"
systemctl stop blumerun2
systemctl disable blumerun2
rm /etc/systemd/system/blumerun2.service
systemctl daemon-reload
echo "Removing Files"
rm -R /usr/local/blumerun
echo "Removing Path"
sed -i 's#export PATH="/usr/local/blumerun/bin:$PATH"##g' ~/.bashrc
. ~/.bashrc
echo Done
echo ----------------------------------------
echo "\nBye Bye!\nYou Can Reinstall here:\n    https://github.com/SamHDev/blumerun/"
