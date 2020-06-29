# Finger Movement Classification via Neural Network using Myo EMG Armband for 3D Printed Robotic Hand

### Introduction
This repository shows a simple and quick method of classifying EMG data coming from Myo Armband using neural networks. The classified finger movement is then sent to a 3-d printed robotic hand that I designed via bluetooth and the robotic hand imitates the finger movement.

![flowchart](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/flowchart.png?raw=true)

### Explanation 
EMG signals are quite random in nature and are difficult to distinguish if we want to use them to differentiate between finger movements. Different sensors have been used by researchers to extract the EMG signals, from painful needle insertion techniques to attaching multiple surface EMG sensors on hand. In this project, a surface EMG based armband is used called "Myo Gesture Control Armband". It was designed by a Canadian company "Thalmic Labs". This armband has 8 sensors that measure EMG signals at 200 Hz frequency.

![armband](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/armband.png?raw=true)

For this project, I used Niklas Rosenstein's Myo-Python library that he kindly shared on Github. This library is based on Python and allows EMG armband to be interfaced using Python programming language. I added some features using his library to make sure application doesnt crash which it would quite often otherwise.
 
The 5 finger movements chosen for thise project were:
1) Thumb open   2) Index finger open  3) Middle finger open  4) Ring finger open  5) Pinky finger open
 
 ![Picture1](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/Picture1.png?raw=true)
 
For 12 finger movement training, we had:
a) Thumb open	b) Index open	c) Middle open	d) Ring open	
e) Pinky open	f) Two fingers open	g) Three fingers open	h) Four fingers open
i) Five fingers open	j) All fingers closed	k) Grab		l) Pick
 
 ![Picture2](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/Picture2.png?raw=true)
 
#### Data Processing
In this project, target was to develop a quick and dirty solution to classify EMG signals that is computationally inexpensive. Here, I record each finger movement's data for 5 seconds. There are two files of codes in repository, one for 5 finger movements and other for 12 finger movements. So, for feature processing I used absolute values of EMG and took windowed average of it with window size of 50. Then i fed the data to train on a neural network.

For neural network, to keep computations less I am using a single hidden layer neural network with 8 neurons and relu activation function. Keras is used for neural network programming. Once that is done, the verification of each finger movement takes one second and classified movement is shown on screen. Also, a signal is sent via bluetooth to Arduino to signal robotic hand to imitate the finger movement.

Following are the training results of neural network 

![results](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/results.png?raw=true)

Following results were observed after training on 5 movements and for 12 movements. Both networks were different:

![confusion matrix](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/confusion%20matrix.jpg?raw=true)

#### Hardware Used:
Following hardware was used for the project:
1) Myo Gesture Control Armband.
2) Futaba S3114 Servo Motors x 5.
3) ABS Material used for 3d printing
4) Arduino Uno
5) HiLetgo Servo motor driver
6) HC-05 Bluetooth module.

Here is a picture of the robotic hand alongwith other hardware

![20190910_112354](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/20190910_112354.jpg?raw=true)

Here is how the design of fingers looks like

![finger design](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/finger%20design.png?raw=true)

Here are different views of palm of robotic hand

![robotic hand](https://github.com/shayanalibhatti/Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand/blob/master/palm%20design.png?raw=true)

Look at the repository to find the code for robotic hand. There are 2 code files for Arduino that run the code for bluetooth data reception and for controlling servo motors for 5 and 12 finger movements. There are 2 code files for Python, one for 5 finger movements, one for 12 finger movements, that take care of receiving bluetooth data from Myo armband and do neural network classification and identify finger movement.

### Working Video
Video of algorithm and robotic hand in action can be viewed on YouTube at https://www.youtube.com/watch?v=4YontNdTQXA

### Conclusion
This project shows a simple method for finger movement classification. It was done to provide a simple EMG classification solution that can be trained without arduous training which can take minutes for people keeping their hand in a static position to train a movement. Thus, a caveat of this method is that the training and verification of each finger movement must be done by keeping hand static on an armchair. It is left to users to increase time of movement for robust results, they can also increase the number of times each movement is recorded to increase the range of movements.

Also, the design of robotic hand that I designed, is quite novel as other designs are huge and use normal servo motors, whereas I used micro servo motor and this hand's dimensions are based on my hand. Thus this design is realistic and very lightweight.

If someone wants to imitate the project, PLEASE CONSIDER USING LSTMs instead of vanilla neural network that i used here. LSTMs have great ability to capture sequences. With Keras, implementing LSTM is very easy. As EMG capture is time-series based data, LSTMs will pave way for better classification and higher number of movements. 

I hope this project and its code will help people using the EMG armband to get a quick start using Myo-Python library and help them achieve their targets with the armband.

### Special Thanks 
Special thanks to Niklas Rosenstein for sharing Myo-Python library on Github.

##### Please give credit and mention my name if you want to imitate the design and/or code. Shoot a message if there are questions.


