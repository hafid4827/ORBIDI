# Prueba Tecnica ORBIDI

## Hola

### Instalamos nuestros paquetes en nuestra virtualizacion

```shell
pip install -r requirements.txt
```

#### Inicializamos celery
```shell
celery -A main.celery worker -l INFO
```

#### Inciamos nuestro servidor
``` shell
uvicorn main:app --reload
```


## En caso estes usando arch linux y otra version de python guarda este escript en algun lugar y usalo para instalar rapidamente pyenv e instalar otra version de python, si puedes mejorarlo te lo agradeceria no es mi fuerte bash a si que agradeceria eso.

``` bash
#!/bin/bash

# recibe un argumento por parte del usuario
URL_repository=$1

# longitud de la cadena de caracteres
len_repository_link=$(expr length $URL_repository)

# filtro de el ultimo elemento de la url/repositorio
repository_name_file=$(echo $URL_repository | grep -b -o "/" | tail -1 | cut -d ":" -f 1)

# acorta con le nombre del directorio basandose el la url
name_short=${URL_repository:repository_name_file:len_repository_link}

# name replace elements
name=$(echo $name_short | cut -d "." -f 1 | tr -d "/.")

git clone $URL_repository && cd $name && makepkg -si && cd .. && rm -rf $name

```