import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import research_agent
import json

def handler(event, context):
    try:
        # Run research to find new topics
        seed_terms = ["AI", "technology", "innovation", "automation", "software"]
        candidates = research_agent.find_topics(seed_terms)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Found {len(candidates)} new candidates',
                'candidates': len(candidates),
                'status': 'success'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Research failed: {str(e)}',
                'status': 'error'
            })
        }