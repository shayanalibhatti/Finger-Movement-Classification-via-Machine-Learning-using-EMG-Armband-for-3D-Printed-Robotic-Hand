# Finger-Movement-Classification-via-Machine-Learning-using-EMG-Armband-for-3D-Printed-Robotic-Hand

### Introduction
This repository shows a simple and quick method of classifying EMG data coming from Myo Armband using neural networks. The classified finger movement is then sent to a 3-d printed robotic hand that I designed via bluetooth and the robotic hand imitates the finger movement.

<< Add flowchart image here >>

### Explanation 
EMG signals are quite random in nature and are difficult to distinguish if we want to use them to differentiate between finger movements. Different sensors have been used by researchers to extract the EMG signals, from painful needle insertion techniques to attaching multiple surface EMG sensors on hand. In this project, a surface EMG based armband is used called "Myo Gesture Control Armband". It was designed by a Canadian company "Thalmic Labs". This armband has 8 sensors that measure EMG signals at 200 Hz frequency.

 <<<<<<<<<< PUT IMAGE OF ARMBAND HERE >>>>>>>>>>>>>>>>>
 
 For this project, I used Niklas Rosenstein's Myo-Python library that he kindly shared on Github. This library is based on Python and allows EMG armband to be interfaced using Python programming language. I added some features using his library to make sure application doesnt crash.
 
#### Data Processing
In this project, target was to develop a quick and dirty solution to classify EMG signals that is computationally inexpensive. Here, I record each finger movement's data for 5 seconds. There are two files of codes in repository, one for 5 finger movements and other for 12 finger movements. So, for feature processing I used absolute values of EMG and took windowed average of it with window size of 50. Then i fed the data to train on a neural network.

For neural network, to keep computations less I am using a single hidden layer neural network with 8 neurons and relu activation function.
Keras is used for neural network programming. Once that is done, the verification of each finger movement takes one second and classified movement is shown on screen. Also, a signal is sent via bluetooth to Arduino to signal robotic hand to imitate the finger movement.

Following are the training results of neural network 
<<< Add performance image here >>>

Following results were observed after training on 5 movements and for 12 movements. Both networks were different:
<< Add confusion matrix here >>

#### Hardware Used:
Following hardware was used for the project:
1) Myo Gesture Control Armband.
2) Futaba S3114 Servo Motors x 5.
3) ABS Material used for 3d printing
4) Arduino Uno
5) HiLetgo Servo motor driver
6) HC-05 Bluetooth module.

Here is a picture of the robotic hand alongwith other hardware
<< Picture of robotic hand >>

Here is how the design of fingers looks like
<< Design of fingers >>

Here are different views of palm of robotic hand
<< Design of palm >>
Look at the repository to find the code and design files for robotic hand. 

### Conclusion
This project shows a simple method for finger movement classification. It 

### Must give credit and mention my name if you want to imitate the design and/or code.

