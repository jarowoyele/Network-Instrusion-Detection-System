from app import create_app
from app.packet_capture import start_capture
import threading
import sys
import os

print(f"Current working directory: {os.getcwd()}")

app = create_app()

if __name__ == '__main__':
    interface = None
    if len(sys.argv) > 1:
        interface = sys.argv[1]

    capture_thread = threading.Thread(target=start_capture, args=(interface,))
    capture_thread.start()
    app.run(debug=True, use_reloader=False)