import keyboard
import sys
import subprocess
import threading
import time
from datetime import datetime

# Get module name from command-line arguments
module_name = sys.argv[1] if len(sys.argv) > 1 else "Default Module"

# Print the module name
print(f"Module: {module_name}")
print("Press 'ESC' to exit the program.")

# Generate timestamped file name
def generate_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"screen_recording_{timestamp}.mp4"

# Screen recording function
def start_screen_recording(output_file, fps=30, screen_region="1920x1080", offset="0,0"):
    command = [
        "ffmpeg",
        "-video_size", screen_region,
        "-framerate", str(fps),
        "-f", "x11grab",
        "-i", f":0.0+{offset}",
        "-vcodec", "libx264",  # Use H.264 codec
        "-preset", "ultrafast",  # Use ultrafast preset for minimal encoding delay
        "-pix_fmt", "yuv420p",  # Ensure compatibility with most players
        output_file
    ]
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print(f"Recording stopped. File saved as {output_file}.")

# Generate the output file name with a timestamp
output_file = generate_filename()

# Start recording in a separate thread
recording_thread = threading.Thread(target=start_screen_recording, args=(output_file,))
recording_thread.start()

# Main loop
try:
    while True:
        if keyboard.is_pressed('esc'):
            print(f"ESC key pressed. {module_name} Exiting...")
            
            # Stop recording by terminating the ffmpeg process
            subprocess.run("pkill -f ffmpeg", shell=True)
            print(f"Screen recording stopped. File saved as {output_file}.")
            
            # Execute the Bash script
            command = f"sudo ./wrapper.sh {module_name} stop"
            try:
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                print(result.stdout)  # Print the output of the Bash script
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                print(e.stderr)  # Print any error messages from the Bash script
            
            break
        time.sleep(0.1)  # Add a slight delay to avoid high CPU usage
except KeyboardInterrupt:
    print("\nProgram interrupted manually.")

