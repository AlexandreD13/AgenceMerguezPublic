docker build -t merguez:worker .

docker run -m 256m -d --name merguez_worker merguez:worker
docker exec -it merguez_worker /bin/bash
docker stop merguez_worker
docker rm merguez_worker
