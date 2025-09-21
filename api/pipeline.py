import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import validation_agent, writer_agent, publisher_agent
import json

def handler(event, context):
    try:
        # Run the complete pipeline
        print("=== Step 1: Validation Agent ===")
        validation_agent.run_validation()

        print("\n=== Step 2: Writer Agent ===")
        writer_agent.run_writer()

        print("\n=== Step 3: Publisher Agent ===")
        publisher_agent.run_publisher()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Pipeline completed successfully!',
                'status': 'success'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Pipeline failed: {str(e)}',
                'status': 'error'
            })
        }