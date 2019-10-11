
from __future__ import print_function
from collections import deque
from threading import Lock, Thread
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import numpy as np
#np.random.seed(1)
import tensorflow as tf
from tensorflow import keras
from keras import regularizers
from keras.models import load_model
from sklearn import preprocessing

import myo
import time
import sys
import psutil
import os
import serial

# This training set will contain 1000 samples of 8 sensor values
global training_set
global number_of_samples
global index_training_set, middle_training_set,thumb_training_set,verification_set
global data_array
number_of_samples = 1000
data_array=[]

Sensor1 = np.zeros((1,number_of_samples))
Sensor2 = np.zeros((1,number_of_samples))
Sensor3 = np.zeros((1,number_of_samples))
Sensor4 = np.zeros((1,number_of_samples))
Sensor5 = np.zeros((1,number_of_samples))
Sensor6 = np.zeros((1,number_of_samples))
Sensor7 = np.zeros((1,number_of_samples))
Sensor8 = np.zeros((1,number_of_samples))

unrecognized_training_set = np.zeros((8,number_of_samples))
index_open_training_set = np.zeros((8,number_of_samples))
middle_open_training_set = np.zeros((8,number_of_samples))
thumb_open_training_set = np.zeros((8,number_of_samples))
ring_open_training_set = np.zeros((8,number_of_samples))
pinky_open_training_set = np.zeros((8,number_of_samples))

verification_set = np.zeros((8,number_of_samples))
training_set = np.zeros((8,number_of_samples))


thumb_open_label = 0
index_open_label = 1
middle_open_label = 2
ring_open_label = 3
pinky_open_label = 4

name = input("Enter name of Subject")

def find_one_hot(labels,classes):
    output = tf.one_hot(labels,classes,axis=0)
    sess = tf.Session()
    out = sess.run(output)
    sess.close
    return out

# This process checks if Myo Connect.exe is running
def check_if_process_running():
    try:
        for proc in psutil.process_iter():
            if proc.name()=='Myo Connect.exe':
                return True            
        return False
            
    except (psutil.NoSuchProcess,psutil.AccessDenied, psutil.ZombieProcess):
        print (PROCNAME, " not running")

# If the process Myo Connect.exe is not running then we restart that process
def restart_process():
    PROCNAME = "Myo Connect.exe"

    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == PROCNAME:
            proc.kill()
            # Wait a second
            time.sleep(1)

    while(check_if_process_running()==False):
        path = 'C:\Program Files (x86)\Thalmic Labs\Myo Connect\Myo Connect.exe'
        os.startfile(path)
        time.sleep(1)

    print("Process started")
    return True

# This is Myo-python SDK’s listener that listens to EMG signal
class Listener(myo.DeviceListener):
    def __init__(self, n):
        self.n = n
        self.lock = Lock()
        self.emg_data_queue = deque(maxlen=n)

    def on_connected(self, event):
        print("Myo Connected")
        self.started = time.time()
        event.device.stream_emg(True)
        
    def get_emg_data(self):
        with self.lock:
            print("H")

    def on_emg(self, event):
        with self.lock:
            self.emg_data_queue.append((event.emg))
            
            if len(list(self.emg_data_queue))>=number_of_samples:
                data_array.append(list(self.emg_data_queue))
                self.emg_data_queue.clear()
                return False



# This method is responsible for training EMG data
def Train(conc_array):
    global training_set
    global index_open_training_set, middle_open_training_set, thumb_open_training_set, ring_open_training_set, pinky_open_training_set, verification_set
    global number_of_samples
    verification_set = np.zeros((8,number_of_samples))
    print (number_of_samples)
    
    labels = []
        
    print(conc_array,conc_array.shape)

    # This division is to make the iterator for making labels run 30 times in inner loop and 10 times in outer loop running total 300 times for 10 finger movements
    samples = conc_array.shape[0]/5
    # Now we append all data in training label
    # We iterate to make 5 finger movement labels.
    for i in range(0,5):
        for j in range(0,int(samples)):
            labels.append(i)
    labels = np.asarray(labels)
    print(labels, len(labels),type(labels))
    print(conc_array.shape[0])
    permutation_function = np.random.permutation(conc_array.shape[0])

    total_samples = conc_array.shape[0]
    all_shuffled_data,all_shuffled_labels = np.zeros((total_samples,8)),np.zeros((total_samples,8))
        
    all_shuffled_data,all_shuffled_labels = conc_array[permutation_function],labels[permutation_function]
    print(all_shuffled_data.shape)
    print(all_shuffled_labels.shape)
    
    number_of_training_samples = np.int(np.floor(0.8*total_samples))        
    train_data = np.zeros((number_of_training_samples,8))
    train_labels = np.zeros((number_of_training_samples,8))
    print("TS ", number_of_training_samples, " S " , number_of_samples)
    number_of_validation_samples = np.int(total_samples-number_of_training_samples)
    train_data = all_shuffled_data[0:number_of_training_samples,:]
    train_labels = all_shuffled_labels[0:number_of_training_samples,]
    print("Length of train data is ", train_data.shape)
    validation_data = all_shuffled_data[number_of_training_samples:total_samples,:]
    validation_labels = all_shuffled_labels[number_of_training_samples:total_samples,]
    print("Length of validation data is ", validation_data.shape , " validation labels is " , validation_labels.shape)
    print(train_data,train_labels)        
        
    model = keras.Sequential([
    # Input dimensions means input columns. Here we have 8 columns, one for each sensor
    keras.layers.Dense(8, activation=tf.nn.relu,input_dim=8,kernel_regularizer=regularizers.l2(0.1)),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(5, activation=tf.nn.softmax)])

    adam_optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    model.compile(optimizer=adam_optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])
        
    history = model.fit(train_data, train_labels, epochs=300,validation_data=(validation_data,validation_labels),batch_size=16)
    model.save('C:/Users/shaya/Desktop/'+name+'_five_finger_model.h5')
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    averages = number_of_samples/50
    # Initializing array for verification_averages
    verification_averages = np.zeros((int(averages),8))
    
    
    while True:
        while True:
            try:
                input("Hold a finger movement and press enter to get its classification")
                hub = myo.Hub()        
                number_of_samples=200
                listener = Listener(number_of_samples)
                hub.run(listener.on_event,20000)

            # Here we send the received number of samples making them a list of 1000 rows 8 columns
                verification_set = np.array((data_array[0]))
                data_array.clear()
                break
            except:
                while(restart_process()!=True):
                    pass
                # Wait for 3 seconds until Myo Connect.exe starts
                time.sleep(3)
                
        verification_set = np.absolute(verification_set)

        div = 50
        # We add one because iterator below starts from 1
        batches = int(number_of_samples/div) + 1
        for i in range(1,batches):
            verification_averages[i-1,:] = np.mean(verification_set[(i-1)*div:i*div,:],axis=0)

        verification_data = verification_averages
        print("Verification matrix shape is " , verification_data.shape)
        
        predictions = model.predict(verification_data,batch_size=16)
        predicted_value = np.argmax(predictions[0])
        print(predictions[0])
        print(predicted_value)
        if predicted_value == 0:
            print("Thumb open")
        elif predicted_value == 1:
            print("Index finger open")
        elif predicted_value == 2:
            print("Middle finger open")
        elif predicted_value == 3:
            print("Ring finger open")
        elif predicted_value == 4:
            print("Pinky finger open")
        else:
            pass

        #### Here i send the predicted value to Arduino via Bluetooth so that it can open appropriate fingers ####

        # While 1 is used because sometimes bluetooth port throws exception in opening the COM Port
        # So i keep trying until the data is sent and confirmation received.
        while(1):
            try:
                # Bluetooth at COM6
                serialPort = serial.Serial(port="COM6",baudrate=9600,bytesize=8,timeout=2,stopbits=serial.STOPBITS_ONE)                
                value_to_bluetooth = str(predicted_value).encode()
                serialPort.write(value_to_bluetooth)
                time.sleep(1)
                if serialPort.in_waiting>0:
                    serialString = serialPort.readline()
                    print(serialString)
                    # If we receive what we sent from Arduino bluetooth then all OK else bad value
                    if serialString == value_to_bluetooth:
                        print("Received")
                    else:
                        print("Bad value")
                serialPort.close()
                break
            except serial.SerialException as e:
                #There is no new data from serial port
                print (str(e))
            except TypeError as e:
                print (str(e))
                ser.port.close()
            

def main():
    index_open_training_set = np.zeros((8,number_of_samples))
    middle_open_training_set = np.zeros((8,number_of_samples))
    thumb_open_training_set = np.zeros((8,number_of_samples))
    ring_open_training_set = np.zeros((8,number_of_samples))
    pinky_open_training_set = np.zeros((8,number_of_samples))
    
    verification_set = np.zeros((8,number_of_samples))
    
    training_set = np.zeros((8,number_of_samples))
    # This function kills Myo Connect.exe and restarts it to make sure it is running
    # Because sometimes the application does not run even when Myo Connect process is running
    # So i think its a good idea to just kill if its not running and restart it

    while(restart_process()!=True):
        pass
    # Wait for 3 seconds until Myo Connect.exe starts
    time.sleep(3)
    
    # Initialize the SDK of Myo Armband
    myo.init('C:\\Users\\shaya\\AppData\\Local\\Programs\\Python\\Python36\\myo64.dll')
    hub = myo.Hub()
    listener = Listener(number_of_samples)

    legend = ['Sensor 1','Sensor 2','Sensor 3','Sensor 4','Sensor 5','Sensor 6','Sensor 7','Sensor 8']

    ################## HERE WE GET TRAINING DATA FOR THUMB FINGER OPEN ########
    while True:
        try:
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            input("Open THUMB ")    
            hub.run(listener.on_event,20000)
            thumb_open_training_set = np.array((data_array[0]))
            print(thumb_open_training_set.shape)
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)
           
    # Here we send the received number of samples making them a list of 1000 rows 8 columns just how we need to feed to tensorflow
    
    ################## HERE WE GET TRAINING DATA FOR INDEX FINGER OPEN ########
    while True:
        try:
            input("Open index finger")
            start_time = time.time()
            hub = myo.Hub()
            listener = Listener(number_of_samples)

            hub.run(listener.on_event,20000)
            # Here we send the received number of samples making them a list of 1000 rows 8 columns 
            index_open_training_set = np.array((data_array[0]))
            
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################## HERE WE GET TRAINING DATA FOR MIDDLE FINGER OPEN #################
    while True:
        try:
            input("Open MIDDLE finger")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            middle_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    # Here we send the received number of samples making them a list of 1000 rows 8 columns
        
    ################## HERE WE GET TRAINING DATA FOR RING FINGER OPEN ##########
    while True:
        try:
            input("Open Ring finger")
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            ring_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    ################### HERE WE GET TRAINING DATA FOR PINKY FINGER OPEN ####################
    while True:
        try:
            input("Open Pinky finger")
            start_time = time.time()
            hub = myo.Hub()
            listener = Listener(number_of_samples)
            hub.run(listener.on_event,20000)
            pinky_open_training_set = np.array((data_array[0]))
            data_array.clear()
            break
        except:
            while(restart_process()!=True):
                pass
            # Wait for 3 seconds until Myo Connect.exe starts
            time.sleep(3)

    
    # Absolute of finger open data
    thumb_open_training_set = np.absolute(thumb_open_training_set)
    index_open_training_set = np.absolute(index_open_training_set)
    middle_open_training_set = np.absolute(middle_open_training_set)
    ring_open_training_set = np.absolute(ring_open_training_set)
    pinky_open_training_set = np.absolute(pinky_open_training_set)

    div = 50
    averages = int(number_of_samples/div)
    thumb_open_averages = np.zeros((int(averages),8))
    index_open_averages = np.zeros((int(averages),8))
    middle_open_averages = np.zeros((int(averages),8))
    ring_open_averages = np.zeros((int(averages),8))
    pinky_open_averages = np.zeros((int(averages),8))

    # Here we are calculating the mean values of all finger open data set and storing them as n/50 samples because 50 batches of n samples is equal to n/50 averages
    for i in range(1,averages+1):
        thumb_open_averages[i-1,:] = np.mean(thumb_open_training_set[(i-1)*div:i*div,:],axis=0)
        index_open_averages[i-1,:] = np.mean(index_open_training_set[(i-1)*div:i*div,:],axis=0)
        middle_open_averages[i-1,:] = np.mean(middle_open_training_set[(i-1)*div:i*div,:],axis=0)
        ring_open_averages[i-1,:] = np.mean(ring_open_training_set[(i-1)*div:i*div,:],axis=0)
        pinky_open_averages[i-1,:] = np.mean(pinky_open_training_set[(i-1)*div:i*div,:],axis=0)
        
     
    # Here we stack all the data row wise
    conc_array = np.concatenate([thumb_open_averages,index_open_averages,middle_open_averages,ring_open_averages,pinky_open_averages],axis=0)
    print(conc_array.shape)
    np.savetxt('C:/Users/shaya/Desktop/'+name+'_five_movements.txt', conc_array, fmt='%i')
    # In this method the EMG data gets trained and verified
    Train(conc_array)

if __name__ == '__main__':
    main()
