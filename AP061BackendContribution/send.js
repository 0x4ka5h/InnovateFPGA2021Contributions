const { BlobServiceClient } = require("@azure/storage-blob");
const connectionString = "DefaultEndpointsProtocol=https;AccountName=ifpgastorshafan;AccountKey=fYIE/xL//fN9CRUByd24GrdWlGGJJFcPClVmTK1QNkQUTLvgbN/fAU7T3CzpuFAye40Q2P5QMibJPCteW3K6QA==;EndpointSuffix=core.windows.net";
const blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);

const containerName = "readingdata"

//const containerClient = blobServiceClient.getContainerClient(containerName);
const blobName = "sensors.json"
async function main() {
  const containerClient = blobServiceClient.getContainerClient(containerName);

  const content = "1";
  const blobName = "a.txt";
  const blockBlobClient = containerClient.getBlockBlobClient(blobName);
  const uploadBlobResponse = await blockBlobClient.upload(content, content.length);
  console.log(`Upload block blob ${blobName} successfully`, uploadBlobResponse.requestId);
}

main();
