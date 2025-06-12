#!/b23yjin/bash

docker exec -it redis-master redis-cli GET user:0
docker exec -it redis-slave1 redis-cli GET user:0
docker exec -it redis-slave2 redis-cli GET user:0
