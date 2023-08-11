import os
import lambda_function_original

print(f"before : {os.environ['LD_LIBRARY_PATH']}")
os.environ['LD_LIBRARY_PATH'] = '/var/task/libvips/lib:' + os.environ.get('LD_LIBRARY_PATH', '')
print(f"after : {os.environ['LD_LIBRARY_PATH']}")

def lambda_handler(event, context):
    return lambda_function_original.lambda_handler(event, context)
