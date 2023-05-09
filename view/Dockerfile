# Use an official Node.js runtime as a parent image
FROM node:16.13.0-alpine

COPY . .
RUN npm install
EXPOSE 3000

CMD ["npm", "run", "start"]