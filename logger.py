from datetime import datetime
import sys
import os

def log_progress(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    # Use absolute path for the log file
    log_file = r"c:\Users\Wajiz.pk\Desktop\Content Generation Pipeline with CrewAI\generation_log.txt"
    
    # Write to file
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
        
    # Also print to terminal
    print(formatted_message)
    sys.stdout.flush()
