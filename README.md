## Order-Checker: paid status en shopify

Este script lee todos los pedidos en estado pendiente desde el 15 de mayo
compara con las ordenes homologas en shopify para determinar si el estado paid se transmitió a centry o no,
Adicionalmente también simula la llamada de actualización de pedido shopify a centry para corregir los casos encontrados.

## Requisitos

Para usar este repo mediante el comando ./Run.sh  se debe tener Docker instalado
[DockerHub](https://docs.docker.com/get-docker/)

## Formato Configs.json

```json
[
    {
        "app_id"          : "{{app_id}}",
        "secret_id"       : "{{secret_id}}",
        "redirect_uri"    : "{{redirect_app_uri}}",
        "tienda-shop"     : "{{tienda-shop}}",
        "apikey-shop"     : "{{apikey-shop}}",
        "pass-shop"       : "{{pass-shop}}"
    },
]
```
