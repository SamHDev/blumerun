echo BlumeRun UnInstaller
echo ----------------------------------------
echo "Removing Service"
systemctl stop blumerun
systemctl disable blumerun
rm /etc/systemd/system/blumerun.service
systemctl daemon-reload
systemctl reset-failed
echo "Removing Files"
rm -R /usr/local/blumerun
echo "Removing Path"
sed -i 's#export PATH="/usr/local/blumerun/bin:$PATH"##g' ~/.bashrc
. ~/.bashrc
echo Done
echo ----------------------------------------
echo "Bye Bye!"
echo "You Can Reinstall here:    https://github.com/SamHDev/blumerun/"
