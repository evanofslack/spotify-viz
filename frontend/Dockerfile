# pull official base image
FROM node:13.12.0-alpine as build

# set working directory
WORKDIR /frontend

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent
RUN npm install react-scripts@3.4.1 -g --silent

# add app
COPY . ./

# Expose port
EXPOSE 3000

# start app
# RUN npm run build
CMD ["npm", "start"]

#
# Production Build
#

# FROM nginx:1.16.0-alpine
# COPY --from=builder /app/build /usr/share/nginx/html
# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx/nginx.conf /etc/nginx/conf.d
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
