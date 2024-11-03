# vaiva-backend


### Docker-compose setup
1. Build docker images for `main-api` and `video-avatar-microservice`. Refer to their README.md files
2. Run all containers: `docker compose up -d`
    * `main-api` logs: `docker logs -f main-api`
    * `video-avatar-microservice` logs: `docker logs -f video-avatar-microservice`
3. To kill containers: `docker compose down`
