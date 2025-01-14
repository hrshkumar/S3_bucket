import boto3
import base64
import json

def lambda_handler(event, context):
    # Initialize the S3 client with LocalStack endpoint
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localstack-main:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test"
    )
    
    try:
        # Validate and extract body from the event
        body = event.get("body")
        if not body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Request body is missing."})
            }
        
        # Decode base64-encoded content
        try:
            file_content = base64.b64decode(body)
        except Exception as decode_error:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid base64 content.", "details": str(decode_error)})
            }
        
        # Extract or default the file name
        file_name = event.get("headers", {}).get("file-name", "uploaded_file.txt")
        
        # Define bucket name
        bucket_name = "test-bucket"  # Replace with your bucket name
        
        # Ensure the bucket exists
        try:
            response = s3.head_bucket(Bucket=bucket_name)
        except Exception as bucket_error:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": f"Bucket '{bucket_name}' does not exist.", "details": str(bucket_error)})
            }
        
        # Upload the file to S3
        try:
            s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        except Exception as upload_error:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Failed to upload file to S3.", "details": str(upload_error)})
            }
        
        # Success response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"File '{file_name}' successfully uploaded to bucket '{bucket_name}'."
            })
        }
    
    except Exception as e:
        # General error handling
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An unexpected error occurred.", "details": str(e)})
        }
