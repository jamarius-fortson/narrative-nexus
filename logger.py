from datetime import datetime
import sys
import os


def log_progress(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"

    # Use relative/configured path for the log file
    log_file = os.getenv(
        "LOG_FILE_PATH",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "generation_log.txt"),
    )

    # Write to file
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

    # Also print to terminal — encode safely for Windows CP1252 terminals
    try:
        print(formatted_message)
    except UnicodeEncodeError:
        safe_message = formatted_message.encode(
            sys.stdout.encoding or "utf-8", errors="replace"
        ).decode(sys.stdout.encoding or "utf-8")
        print(safe_message)
    sys.stdout.flush()
