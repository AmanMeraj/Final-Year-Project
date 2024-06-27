import serial
import csv
import threading
import time


serial_port = 'COM3'  
baud_rate = 9600


lock = threading.Lock()


def read_serial_and_write_csv():
    try:
        
        ser = serial.Serial(serial_port, baud_rate, timeout=1)  
        
        with open('sensor_data.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            
            writer.writerow(['temp', 'humidity', 'spO2', 'wound temp', 'type'])
            
            start_time = time.time()  
           
            while True:
               
                line = ser.readline().decode().strip()
                
                
                if line:
                  
                    values = line.split(',')
                    
                   
                    with lock:
                        writer.writerow(values)
                
                if time.time() - start_time >= 20:
                    break 
    except serial.SerialException as e:
        print("Error: Unable to open serial port. Make sure it is not already in use.")
        exit()
    except PermissionError:
        print("Error: Permission denied. Make sure you have the necessary permissions to access the file.")
        exit()
    except Exception as e:
        print("Error:", e)

serial_thread = threading.Thread(target=read_serial_and_write_csv)
serial_thread.start()

serial_thread.join()
