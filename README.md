git clone https://github.com/lidiaPolyakov/Products-project.git -b mongo-cloud 

Open 2 terminals - one for the client and one for the serve

server:
cd Products-project/server
npm install

Please add the .env file into the server directory.
the .env contains the DB connection user:
MONGO_USERNAME=lidiapolykov
MONGO_PASSWORD=bNwbrKQL5mgUvgzn


client:

cd Products-project/client
npm install
npm start
