# Finger Movement Classification via Neural Network using Myo EMG Armband for 3D Printed Robotic Hand

### Introduction
This repository shows a simple and quick method of classifying EMG data coming from Myo Armband using neural networks. The classified finger movement is then sent to a 3-d printed robotic hand that I designed via bluetooth and the robotic hand imitates the finger movement.

![flowchart](https://user-images.githubusercontent.com/41015749/66622987-681c4c80-ebaf-11e9-8ee5-1998cdfc2ac2.png)

### Explanation 
EMG signals are quite random in nature and are difficult to distinguish if we want to use them to differentiate between finger movements. Different sensors have been used by researchers to extract the EMG signals, from painful needle insertion techniques to attaching multiple surface EMG sensors on hand. In this project, a surface EMG based armband is used called "Myo Gesture Control Armband". It was designed by a Canadian company "Thalmic Labs". This armband has 8 sensors that measure EMG signals at 200 Hz frequency.

![armband](https://user-images.githubusercontent.com/41015749/66623030-8bdf9280-ebaf-11e9-9288-cdeb6f932af4.png)

For this project, I used Niklas Rosenstein's Myo-Python library that he kindly shared on Github. This library is based on Python and allows EMG armband to be interfaced using Python programming language. I added some features using his library to make sure application doesnt crash which it would quite often otherwise.
 
The 5 finger movements chosen for thise project were:
1) Thumb open   2) Index finger open  3) Middle finger open  4) Ring finger open  5) Pinky finger open
 
 ![Picture1](https://user-images.githubusercontent.com/41015749/66705672-5a6de080-ecef-11e9-8732-b253c6e4dec9.png)
 
For 12 finger movement training, we had:
a) Thumb open	b) Index open	c) Middle open	d) Ring open	
e) Pinky open	f) Two fingers open	g) Three fingers open	h) Four fingers open
i) Five fingers open	j) All fingers closed	k) Grab		l) Pick
 
 ![Picture2](https://user-images.githubusercontent.com/41015749/66705674-5c37a400-ecef-11e9-825e-07724736ec94.png)
 
#### Data Processing
In this project, target was to develop a quick and dirty solution to classify EMG signals that is computationally inexpensive. Here, I record each finger movement's data for 5 seconds. There are two files of codes in repository, one for 5 finger movements and other for 12 finger movements. So, for feature processing I used absolute values of EMG and took windowed average of it with window size of 50. Then i fed the data to train on a neural network.

For neural network, to keep computations less I am using a single hidden layer neural network with 8 neurons and relu activation function. Keras is used for neural network programming. Once that is done, the verification of each finger movement takes one second and classified movement is shown on screen. Also, a signal is sent via bluetooth to Arduino to signal robotic hand to imitate the finger movement.

Following are the training results of neural network 

![results](https://user-images.githubusercontent.com/41015749/66623043-9b5edb80-ebaf-11e9-909f-e4206ddf390a.png)

Following results were observed after training on 5 movements and for 12 movements. Both networks were different:

![confusion matrix](https://user-images.githubusercontent.com/41015749/66623050-a580da00-ebaf-11e9-815e-ea612c73b644.jpg)

#### Hardware Used:
Following hardware was used for the project:
1) Myo Gesture Control Armband.
2) Futaba S3114 Servo Motors x 5.
3) ABS Material used for 3d printing
4) Arduino Uno
5) HiLetgo Servo motor driver
6) HC-05 Bluetooth module.

Here is a picture of the robotic hand alongwith other hardware

![20190910_112354](https://user-images.githubusercontent.com/41015749/66623057-afa2d880-ebaf-11e9-8382-a1852b5388de.jpg)

Here is how the design of fingers looks like

![finger design](https://user-images.githubusercontent.com/41015749/66623074-bf222180-ebaf-11e9-9fce-445f176eea32.jpg)

Here are different views of palm of robotic hand

![robotic hand](https://user-images.githubusercontent.com/41015749/66623082-cba67a00-ebaf-11e9-9a7d-74349d522b87.jpg)

Look at the repository to find the code for robotic hand. There are 2 code files for Arduino that run the code for bluetooth data reception and for controlling servo motors for 5 and 12 finger movements. There are 2 code files for Python, one for 5 finger movements, one for 12 finger movements, that take care of receiving bluetooth data from Myo armband and do neural network classification and identify finger movement.

### Conclusion
This project shows a simple method for finger movement classification. It was done to provide a simple EMG classification solution that can be trained without arduous training which can take minutes for people keeping their hand in a static position to train a movement. Thus, a caveat of this method is that the training and verification of each finger movement must be done by keeping hand static on an armchair. It is left to users to increase time of movement for robust results, they can also increase the number of times each movement is recorded to increase the range of movements.

I hope this project and its code will help people using the EMG armband to get a quick start using Myo-Python library and help them achieve their targets with the armband.

### Special Thanks 
Special thanks to Niklas Rosenstein for sharing Myo-Python library on Github.

##### Please give credit and mention my name if you want to imitate the design and/or code. Shoot a message if there are questions.


