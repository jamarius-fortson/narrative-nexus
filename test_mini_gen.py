import os
import sys
from dotenv import load_dotenv
from content_generation_crew import ContentGenerationCrew
from logger import log_progress

def test_mini():
    load_dotenv()
    log_progress("Starting Mini Test...")
    try:
        crew_obj = ContentGenerationCrew()
        topic = "Healthy Breakfast Ideas"
        log_progress(f"Testing with topic: {topic}")
        
        result = crew_obj.generate_content(topic, "Blog Post")
        log_progress("Generation finished.")
        print("\n--- RESULT ---")
        print(result["final_content"][:500])
        print("\n--- END ---")
    except Exception as e:
        log_progress(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mini()
