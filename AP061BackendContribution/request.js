const { BlobServiceClient } = require("@azure/storage-blob");
const connectionString = "DefaultEndpointsProtocol=https;AccountName=ifpgastorshafan;AccountKey=fYIE/xL//fN9CRUByd24GrdWlGGJJFcPClVmTK1QNkQUTLvgbN/fAU7T3CzpuFAye40Q2P5QMibJPCteW3K6QA==;EndpointSuffix=core.windows.net";
const blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);

const containerName = "readingdata"

//const containerClient = blobServiceClient.getContainerClient(containerName);
const blobName = "sensors.json"
async function main() {
  const containerClient = blobServiceClient.getContainerClient(containerName);
  const blobClient = containerClient.getBlobClient(blobName);

  // Get blob content from position 0 to the end
  // In Node.js, get downloaded data by accessing downloadBlockBlobResponse.readableStreamBody
  const downloadBlockBlobResponse = await blobClient.download();
  const downloaded = (
    await streamToBuffer(downloadBlockBlobResponse.readableStreamBody)
  ).toString();
  console.log(downloaded);
  
  //downloaded varible 

  async function streamToBuffer(readableStream) {
    return new Promise((resolve, reject) => {
      const chunks = [];
      readableStream.on("data", (data) => {
        chunks.push(data instanceof Buffer ? data : Buffer.from(data));
      });
      readableStream.on("end", () => {
        resolve(Buffer.concat(chunks));
      });
      readableStream.on("error", reject);
    });
  }
}

main();

