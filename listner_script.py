import serial

PORT = "COM5"   # <-- change this to your port

ser = serial.Serial(PORT, 115200, timeout=1)
print("Listening for button... (press Stop to quit)")

while True:
    line = ser.readline().decode(errors="ignore").strip()
    if line == "INSPECT":
        print("Button pressed!")