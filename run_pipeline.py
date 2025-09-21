from agents import validation_agent, writer_agent, publisher_agent

def run_pipeline():
    print("=== Step 1: Validation Agent ===")
    validation_agent.run_validation()

    print("\n=== Step 2: Writer Agent ===")
    writer_agent.run_writer()

    print("\n=== Step 3: Publisher Agent ===")
    publisher_agent.run_publisher()

    print("\n=== Pipeline complete! Check Ghost CMS for published posts. ===")

if __name__ == "__main__":
    run_pipeline()