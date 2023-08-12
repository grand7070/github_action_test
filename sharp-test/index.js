'use strict';

const querystring = require('querystring');
const AWS = require('aws-sdk');
const Sharp = require('sharp');

const S3 = new AWS.S3({
  region: 'ap-northeast-2'
});
const BUCKET = 'test-le';

exports.handler = async (event, context, callback) => {
  const { request, response } = event.Records[0].cf;
  if (Number(response.status) !== 200) {
    console.error(`response status is ${response.status}, not 200`);
    return callback(null, response);
  }
  
  // Parameters are w, h, f, q and indicate width, height, format and quality.
  const params = querystring.parse(request.querystring);
  
  // Required width or height value.
  if (!params.w || !params.h) {
    console.error(`query parameter is wrong. w,h,f,q : ${params.w},${params.h},${params.f},${params.q}`);
    return callback(null, response);
  }

  // Extract name and format.
  const { uri } = request;
  const [, imageName, extension] = uri.match(/\/?(.*)\.(.*)/);

  // Init variables
  let width;
  let height;
  // let format;
  let quality; // Sharp는 이미지 포맷에 따라서 품질(quality)의 기본값이 다릅니다.
  let s3Object;
  let resizedImage;

  // Init sizes.
  width = parseInt(params.w, 10) ? parseInt(params.w, 10) : null;
  height = parseInt(params.h, 10) ? parseInt(params.h, 10) : null;

  // Init quality.
  quality = parseInt(params.q, 10) ? parseInt(params.q, 10) : 95;
  if (quality > 95) {
    quality = 95;
  }
  if (quality < 10) {
    quality = 10;
  }

  // Init format.
  // format = params.f ? params.f : extension;
  // format = format === 'jpg' ? 'jpeg' : format;

  // For AWS CloudWatch.
  console.log(`parmas: ${JSON.stringify(params)}`); // Cannot convert object to primitive value.
  console.log(`name: ${imageName}.${extension}`); // Favicon error, if name is `favicon.ico`.

  try {
    s3Object = await S3.getObject({
      Bucket: BUCKET,
      Key: decodeURI(imageName + '.' + extension)
    }).promise();
  } catch (error) {
    console.error('S3.getObject: ', error);
    // return callback(error);
    return callback(null, response);
  }

  try {
    resizedImage = await Sharp(s3Object.Body)
      .resize(width, height)
      .toFormat("jpeg", {
        quality
      })
      .toBuffer();
  } catch (error) {
    console.error('Sharp: ', error);
    // return callback(error);
    return callback(null, response);
  }

  const resizedImageByteLength = Buffer.byteLength(resizedImage, 'base64');
  console.log('byteLength: ', resizedImageByteLength);

  // `response.body`가 변경된 경우 1MB까지만 허용됩니다.
  if (resizedImageByteLength >= 1 * 1000 * 1000) {
    // TODO
    console.log(`image size ${resizedImageByteLength} is upper than 1MB`);
    return callback(null, response);
  }

  response.status = 200;
  response.body = resizedImage.toString('base64');
  response.bodyEncoding = 'base64';
  response.headers['content-type'] = [
    {
      key: 'Content-Type',
      value: `image/jpeg`
    }
  ];
  return callback(null, response);
};
