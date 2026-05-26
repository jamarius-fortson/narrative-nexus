from content_generation_crew import ContentGenerationCrew
import sys

def test_generation():
    print("Initializing Crew...")
    try:
        crew = ContentGenerationCrew()
        print("Crew initialized successfully.")
        
        # Run a very short, simple task to verify the tool and agents work
        topic = "The color of the sky"
        # We use a mocked content type that implies brevity to save cost/time
        content_type = "short fact" 
        
        print(f"Starting generation for topic: {topic}")
        result = crew.generate_content(topic, content_type)
        
        print("\nGeneration Result:")
        print(result['final_content'][:200] + "...") # Print first 200 chars
        print("\nSUCCESS: Pipeline verified.")
        
    except Exception as e:
        print(f"\nFAILURE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_generation()
