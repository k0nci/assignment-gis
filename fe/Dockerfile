# build stage
FROM node:11.6-alpine as build-stage

WORKDIR /app
COPY hstorms ./

RUN npm install
RUN npm run build


# production stage
FROM nginx:1.15-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]