<p align="center">
  <img src="https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/256x256.png">
</p>

# A brief introduction to Secure-PI
Secure-PI is a raspberry pi based project powered by google TensorFlow, in other words, a security camera with human recognition based on AI detection.
The way it works is that it takes pictures whenever human presence is detected in the camera's field of view. All the pictures have a timestamp and can be found on the web interface giving the user the ability to remotely see what is happening. Besides that, it also features a live view and an SMTP server which serves to send e-mails to the users if the IP address has changed, due to the fact that most ISP uses DHCP to randomly allocate the IP addresses and some of them change the IP's quite often, this way we provide a stable connection to the camera.
![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/secure-pi.png)

# Required materials
To get started we gonna need some materials such as:
1. [Raspberry pi 3b+](https://www.ebay.co.uk/itm/123903810192)
2. [Raspberry pi camera module](https://thepihut.com/products/raspberry-pi-camera-module?variant=758603005) *you could buy a regular one, but I highly recommend the one with night vision*
3. [Power supply](https://thepihut.com/products/raspberry-pi-psu-eu)
4. MicroSD Card
5. I suggest you buy weather [a case which comes with a fan](https://www.ebay.co.uk/itm/For-Raspberry-Pi-3-Model-B-Plus-Acrylic-Case-Transparent-Box-Cover-Shell-V05/323857535501?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2060353.m2749.l2649) or at least heatsinks thus the temperatures can get high and **it could damage the board.**


# Flashing the OS to the MicroSD card and testing the camera connection

### After we gathered all the materials we can get started by putting all those pieces together and installing the operating system.
- First of all download the latest version of Raspbian which can be found here:

~~~
https://www.raspberrypi.org/downloads/raspbian/
~~~

- After that, we have to download balena etcher to write the os image to the MicroSD card

~~~
https://www.balena.io/etcher/
~~~

- Flash the image

![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/1.png)


### We'll perform a headless installation


- Open the **card** and create two files in the **boot folder**, one called **ssh without any extension**, which will grant us ssh access later on and another one called **wpa_supplicant.conf** which will take care of the internet connection.
- Open **wpa_supplicant.conf** and paste the following code and fill it with your *wireless credentials and country*

```
country=gb
update_config=1
ctrl_interface=/var/run/wpa_supplicant

network={
 ssid="<Name of your WiFi>"
 psk="<Password for your WiFi>"
}
```

![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/3.png)

- Save, exit and plug the card into the Pi and boot it up

More information about this process can be found on raspberry pi documentation:

~~~
https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
~~~

- After you plug in the power supply go to **command prompt** and type 
~~~
arp -a
~~~

Something similar to this should show up, try to ssh all the IPs listed with dynamic type to find out which one was assigned to the pi. In my case was **192.168.1.133**

![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/4.png)

*You could also use angry IP scanner to find out which IP was assigned to the board*
![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/4a.png)

- With **putty** establish a ssh into the pi

*The credentials are pi:raspberry*

![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/5.png)

- The next step is to test the camera to see if everything is all righ, in order to do so type the following command into the terminal
~~~
raspistill -o test.jpg
~~~
*If no error shows up we can look over the file to see if it exists using ls, which means that everything is all right*
![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/7.png)

- At this point, we have to update and upgrade the pi

~~~
sudo apt-get update
sudo apt-get upgrade
~~~

*This may take a while so be patient. Once everything is done reboot the pi and we can get started installing secure-pi*

# Installing secure-pi
- First of all, we have to download the installation file
~~~
wget https://raw.githubusercontent.com/Terkea/secure-pi/master/install.sh
~~~
- Execute the shell file
~~~
sudo bash install.sh
~~~

*The whole process might take between 10-20 minutes so meanwhile, be sure that you leave it alone to download all the requirements and install the service*

- Navigate to the IP address assigned to the pi>settings and set up the **SMTP server** with your credentials

*login credentials: secure@pi.com:raspberry*
![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/9.png)

- To make the pi visible outside our private network, we have to set up a port forwarding rule. To do this we have to log in into our router, then go to firewall. Add the raspberry pi's IP address and the running port which is by default set to 5000 save and restart the router.
![alt text](https://raw.githubusercontent.com/Terkea/secure-pi/master/tutorial/10.png)

*Your router interface would most likely look different but the process is just the same*

Now we are all set and done. Congrats, you just got yourself a security camera with artificial intelligence

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
