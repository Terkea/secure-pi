# /bin/sh
echo -e "Installing requirements"
sudo apt-get install -y python3-pip git
pip3 install opencv-python
sudo apt-get install -y libcblas-dev
sudo apt-get install -y libhdf5-dev
sudo apt-get install -y libhdf5-serial-dev
sudo apt-get install -y libatlas-base-dev
sudo apt-get install -y libjasper-dev
sudo apt-get install -y libqtgui4
sudo apt-get install -y libqt4-test
sudo pip3 install flask flask_jsglue flask_sqlalchemy flask_wtf
sudo pip3 install bcrypt imageio
sudo pip3 install tensorflow
sudo git clone https://github.com/Terkea/secure-pi.git /opt/secure-pi
SERVICE_FILE="/lib/systemd/system/secure-pi.service"
echo "Creating the service"
/bin/cat <<EOM >> $SERVICE_FILE
[Unit]
After=multi-user.target

[Service]
Type=idle
ExecStart=/opt/secure-pi/start.sh
User=pi

[Install]
WantedBy=multi-user.target
EOM
sudo systemctl daemon-reload
sudo systemctl enable secure-pi.service
echo "All set an done"
