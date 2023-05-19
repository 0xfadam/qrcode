from pyzbar.pyzbar import decode
import cv2
import zlib
import base64

# Initialize the camera
camera = cv2.VideoCapture(0)

# Initialize QR code detection variables
qr_code_data_list = []
qr_code_detected = False

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()

    # Decode the QR code
    decoded_data = decode(frame)

    # Check if a QR code is found
    if decoded_data:
        qr_code_data = decoded_data[0].data.decode("utf-8")

        if not qr_code_detected:
            qr_code_detected = True
            print("QR Code detection started.")

        if qr_code_data not in qr_code_data_list and qr_code_data!= "eJwLjvRz1jEAAAY+AZo=":
            qr_code_data_list.append(qr_code_data)
            print("QR Code data:", qr_code_data)

    # Display the current decoded QR code value
    if qr_code_detected:
        cv2.putText(frame, "QR Code: " + qr_code_data, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Camera', frame)

    # Check for 'q' key press
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the camera
camera.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

# Process and save the QR code data
filename = input("Enter the output filename: ")
with open(filename, "wb") as file:
    for qr_code_data in qr_code_data_list:
        if qr_code_data != "SYNC,0":
            # Decode from base64 and decompress the data
            decoded_data = base64.b64decode(qr_code_data)
            decompressed_data = zlib.decompress(decoded_data)
            file.write(decompressed_data)

print(f"QR Code data saved to '{filename}'")
