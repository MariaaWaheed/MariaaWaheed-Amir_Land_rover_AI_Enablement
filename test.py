import cv2
import time

def capture_images(interval):
    # Open a connection to the default camera (index 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    # Set video frame width and height (optional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

    img_counter = 0

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Failed to capture image.")
                break

            # Display the captured frame (optional)
            cv2.imshow('Captured Image', frame)

            # Save the frame as an image file
            img_name = f"image_{img_counter:04d}.png"
            cv2.imwrite(img_name, frame)
            print(f"Saved {img_name}")

            img_counter += 1

            # Wait for the specified interval
            time.sleep(interval)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        # Handle the interruption (e.g., by pressing Ctrl+C)
        print("Capture interrupted.")

    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

# Set the interval (in seconds) here
capture_interval = 3
capture_images(capture_interval)
