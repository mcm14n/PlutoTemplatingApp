# Pull latest official node image
FROM node:14-slim

# Expose ports
EXPOSE 3000

# Set working directory
RUN mkdir /pluto
WORKDIR /pluto

# add `/app/node_modules/.bin` to environment variables
ENV PATH /pluto/node_modules/.bin:$PATH

# Copy package files and install app dependencies
# Add React app to working directory
ADD . /pluto
RUN npm install
RUN npm install react-scripts -g


# Start the React app
CMD ["npm", "start"]