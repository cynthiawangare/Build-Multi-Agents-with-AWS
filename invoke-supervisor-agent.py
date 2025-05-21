import json
import boto3

def lambda_handler(event, context):
    data = event['body']
    data_dict = json.loads(data) # this is data received from user
    input_text = data_dict['text'] #questions asked by user
    session_id = data_dict['sessionId']
    client = boto3.client('bedrock-agent-runtime')

    try:
        response = client.invoke_agent(
            agentId='9PUBCJW6RB', # copy the Id of the supervisor agent
            agentAliasId='AJRT6NLBG1', # copy the supervisor agent alias id and paste here
            sessionId=session_id,
            endSession=False,
            inputText=input_text
        )

        response_text = ""

        for event in response.get('completion',[]):
            if "chunk" in event and "bytes" in event['chunk']:
                # Decode bytes to string using UTF-8
                response_text += event['chunk']['bytes'].decode('utf-8')
        
        print(response_text)

        return {
            'statusCode': 200,
            'body': json.dumps({
                "response": response_text
            })
        }

    except Exception as e:
        return{
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }

    
