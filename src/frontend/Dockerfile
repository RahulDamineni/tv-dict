FROM node:latest

ADD . tv_dict/src/frontend

# WORKDIR tv_dict/src/frontend

# add `/app/node_modules/.bin` to $PATH
# ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
# COPY package.json ./
# COPY package-lock.json ./
WORKDIR tv_dict/src/frontend
RUN npm install --silent


# add app
# COPY . ./
# RUN npm run build

# start app
CMD ["npm", "start"]