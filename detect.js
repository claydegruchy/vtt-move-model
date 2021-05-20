const vision = require('@google-cloud/vision');

// Creates a client
const client = new vision.ImageAnnotatorClient();

/**
 * TODO(developer): Uncomment the following line before running the sample.
 */
const fileName = './test_images/IMG_1358.JPG';

// Performs logo detection on the local file
const [result] = await client.logoDetection(fileName);
const logos = result.logoAnnotations;
console.log('Logos:');
logos.forEach(logo => console.log(logo));
