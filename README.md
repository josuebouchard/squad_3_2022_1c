# Módulo de soporte de PSA

- Squad: 3
- Tribu: 1
- Modulo: Soporte

## Pipenv

Este sistema utiliza un entorno virtual de python (pipenv).

Para instalar las dependencias, corra el siguiente comando:
```bash
pipenv install
```

Para abrir una terminal dentro de ese entorno, corra el comando:
```bash
# Para entrar
pipenv shell

# Para salir
exit
```

O si prefiere correr un comando sin tener que hacer lo anterior, se puede proceder a ejecutar:
```bash
pipenv run <COMANDO>
```

## Configuracion de base de datos

Para conectarse a la base de datos, el sistema debe recibir como variable de entorno (o en su defecto, en un `.env` ubicado en la raiz del proyecto):
```ini
DATABASE_URL="postgresql://<USUARIO>:<CONTRASEÑA>@<HOST>:<PUERTO>/<DBNAME>"
```

## Como correr las pruebas de BDD

Este sistema utiliza [Behave](https://github.com/behave/behave) como framework de BDD.
Los archivos Gherkin se encuentran en `./tests/feature`.

Para correr las pruebas, estando parado en la raiz del proyecto (a la altura de este README), se procede a correr el comando:
```bash
pipenv run behave ./tests/feature
```

## Correr el servidor

Para correr el servidor, se procede a ejecutar:
```bash
uvicorn psa_soporte.main:app --host=0.0.0.0 --port=<PUERTO> --env-file=".env"
```