'''!
    @file       main.py
    @brief      The main script on the microcontroller board to print out step response using a timer callback.
    @details    This file is stored on the microcontroller. There is blocking code that waits for a serial port
                input. When something is written through the serial port, the input pin connecting to the RC
                circuit is set to high (5V) for about two seconds and then sets it back to low. Meanwhile, there
                is a timer interupt that runs at 1000Hz collecting the ADC value and storing it in a queue. The
                data from the queue will then be printed out through the serial port after the step response.
    @author Damond Li
    @author Chris Or
    @author Chris Suzuki
    @date 1/25/22
'''
import pyb
import time
import task_share

# Timer Callback
def ticker(timerobj):
    '''!
        @brief   Timer callback to collect the data from the step response
        @details This is a callback function for the timer which reads from the ADC
                 and places the value in a queue. If the queue is full, no data is
                 put in the queue to prevent our script from blocking.
    '''
    
    # Place the data in the queue if it is not full
    if not adcqueue.full():
        adcqueue.put(ADC.read(), in_ISR=True)
        
def print_data():
    '''!
        @brief   Function for printing collected data
        @details This function prints the each of the collected data as well as a
                 value which for the time. Because the timer callback is run at 1000Hz,
                 it is assumed that each value in the queue corresponds with a delta time of
                 1 millisecond. There is a marker that gets printed at the very end which
                 indicates that all the data has been printed. This is important because on
                 the PC side, if the readline() function is run with nothing in the serial port,
                 it blocks the whole script from running.
    '''
    
    ## Variable representing the time in milliseconds
    time_ms = 0
    while not adcqueue.empty():
        print(str(time_ms) + "," + str(adcqueue.get()))
        time_ms += 1
    print("DATA")


if __name__ == '__main__':
    
    while True:
        
        input()
        
        # Establish timer
        ## Timer object for the timer callback
        timer = pyb.Timer(1, freq=1000)
        
        # Establish input pin
        ## The pin object for the input to the RC circuit
        pinC1 = pyb.Pin(pyb.Pin.cpu.C1)
        
        # Establish output pin to read ADC value
        ## The pin object which will be responsible for reading the voltage level
        pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
        
        # Establish ADC
        ## The ADC object which will read the ADC value
        ADC = pyb.ADC(pinC0)
        
        # Create queues
        ## A queues object to store the step response voltage over time
        adcqueue = task_share.Queue ('L', 1500, thread_protect = False, overwrite = False,
                                   name = "ADC Queue")
        
        # *** Actual Code Begins ***
        
        # Establish start reference time
        ## A reference starting time
        start_time = time.time()

        # Timer interupt
        timer.callback(ticker)
        
        # Set the input pin to high
        pinC1.high()
        
        # Establish how long to run the step response
        while time.time() - start_time < 2:
            pass

        # End the timer callback
        timer.callback(None)
        
        # Set pin low
        pinC1.low()
        
        # Print data through serial port
        print_data()


    





    
    

