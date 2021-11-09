# Docker-Compose

## Docker Compose
Se ejecuta despues de realizar cambios en el código, para reconstruir una imagen en base al docker-file, y si no esta la crea.
``` sh
docker-compose build
```

Ejecuta nuestra imagen creada en base al docker-file y lo ejecuta en segundo plano
``` sh
docker-compose up -d
```

Detener los contenedores
``` sh
docker-compose stop
```

## Docker
Listar contenedores en ejecución
``` sh
docker ps
```

Listar contenedores que no se estan ejecutando
``` sh
docker ps -a
```

Para ingresar a un contenedor se ejecuta lo siguiente
``` sh
docker exec -it ContainerID bash
```

## Ingresar a Postgres
Para ingresar a la base de datos del contenedor ejecutar el comando

``` sh
psql -h localhost -d Proyecto -U root -p 5432
```

Una vez dentro de postgres, ya se puede ejecutar cualquier sentencia de SQL