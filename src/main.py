import pyb
import time
import task_share
# import micropython

# Timer Callback
def ticker(timerobj):
    if not adcqueue.full():
        adcqueue.put(ADC.read(), in_ISR=True)
        
def print_data():
    time_ms = 0
    while not adcqueue.empty():
        print(str(time_ms) + "," + str(adcqueue.get()))
        time_ms += 1
    print("DATA")


if __name__ == '__main__':
    
    # micropython.alloc_emergency_exception_buf(100)
    
    while True:
        
        input()
        
        # Establish timer
        timer = pyb.Timer(1, freq=1000)
        
        # Establish input pin
        pinC1 = pyb.Pin(pyb.Pin.cpu.C1)
        
        # Establish output pin to read ADC value
        pinC0 = pyb.Pin(pyb.Pin.cpu.C0)
        
        # Establish ADC
        ADC = pyb.ADC(pinC0)
        
        # Create queues
        adcqueue = task_share.Queue ('L', 1500, thread_protect = False, overwrite = False,
                                   name = "ADC Queue")
        
        # *** Actual Code Begins ***
        
        # Establish start reference time
        start_time = time.time()

        # Timer interupt
        timer.callback(ticker)
        
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


    





    
    

