
from urllib import parse
import boto3
import base64
import io
import pyvips

os.environ['LD_LIBRARY_PATH'] = '/var/task/libvips/lib'
s3_bucket_name = "test-le"
s3_client = boto3.client("s3")


def get_s3_object(s3_object_key):
    try:
        return s3_client.get_object(Bucket=s3_bucket_name, Key=parse.unquote(s3_object_key))
    except Exception as e:
        print("get_s3_object Exception", e)


def resize_image(original_image, w, h, q):
    try:
        image = pyvips.Image.thumbnail_buffer(original_image, w, height=h, size="force")

        bytes_io = io.BytesIO()
        image.jpegsave_target(pyvips.Target.new_to_memory(bytes_io), Q=q)

        result_size = bytes_io.tell()
        result_data = bytes_io.getvalue()
        result = base64.standard_b64encode(result_data).decode()
        bytes_io.close()
        res = {'resized_image': result, 'resized_image_size': result_size}
        return res
    except Exception as e:
        print(e)
        return None


def get_image_arguments(queries):
    w, h, q = 0, 0, 95
    if not queries:
        return w, h, q
    for query in queries.split("&"):
        for key, value in query.split("="):
            if key in ('w', 'h', 'q'):
                key = int(value)

    if q >= 95: q = 95
    if q < 10: q = 10

    return w, h, q


def lambda_handler(event, context):
    request = event["Records"][0]["cf"]["request"]
    response = event["Records"][0]["cf"]["response"]

    if int(response['status']) != 200: # TODO
        print(f"response status is {response['status']}, not 200")
        return response

    w, h, q = get_image_arguments(request['querystring'])
    if w == 0 or h == 0:
        print(f"query parameter is wrong. w,h,q : [{w, h, q}]")
        return response

    s3_object_key = request['uri'][1:]
    s3_response = get_s3_object(s3_object_key)

    if not s3_response:
        return response

    s3_object_type = s3_response["ContentType"]
    if s3_object_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return response

    result = resize_image(s3_response['Body'].read(), w, h, q)

    if not result:
        return response

    resized_image = result['resized_image']
    resized_image_size = result['resized_image_size']

    if resized_image_size > 1000 * 1000:
        s3_object_key_split = s3_object_key.split("/")
        s3_object_key_split[-1] = "resized_" + s3_object_key_split[-1]
        converted_object_key = "/".join(s3_object_key_split)

        try:
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key=parse.unquote(converted_object_key),
                ContentType=s3_object_type,
                Body=base64.b64decode(resized_image),
            )
        except Exception as e:
            print(e)

        response["status"] = 301
        response["statusDescription"] = "Moved Permanently"
        response["body"] = ""
        response["headers"]["location"] = [
            {"key": "Location", "value": f"/{converted_object_key}"}
        ]
        return response

    response["status"] = 200
    response["statusDescription"] = "OK"
    response["body"] = resized_image
    response["bodyEncoding"] = "base64"
    response["headers"]["content-type"] = [
        {"key": "Content-Type", "value": s3_object_type}
    ]

    return response
