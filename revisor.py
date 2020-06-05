#!/usr/bin/env python
# -*- coding: utf-8 -*- 


# from __future__ import unicode_literals
# import xlsxwriter
import requests
from CentrySDK import Centry
import json
from time import sleep , time
import concurrent.futures
import threading
import traceback, sys



def sendNotify(i):
    payload = "{\n    \"id\": "+i.strip()+"\n}"
    headers = {
	    'content-type': "application/json"
    }
    url = "https://www.centry.cl/conexion/shopify_callback/"+Company_id+"/onOrderUpdated"
    response = requests.request("POST", url, data=payload, headers=headers)
    # print( response.status_code )
    if response.status_code != 200:
        sleep(1)
        sendNotify(i)
    # print(i)
	

def orderChecker(order):
    #print(order["status_origin"] + " " + order["id_origin"] + " " +company["tienda-shop"] )
    if("pending" in order["status_origin"]):
        url_order_shop = "https://" + company["apikey-shop"]+ ":" + company["pass-shop"]+ "@" + company["tienda-shop"]+ ".myshopify.com/admin/orders/"+order["id_origin"] +".json"
        #print (url_order_shop)
        response = requests.request("GET", url_order_shop)
        if(response.status_code == 200):
            shop_order= json.loads(response.text)
         #   print(shop_order["order"]["financial_status"])
            if (shop_order["order"]["financial_status"] == "paid"):
                Resultados[order["_id"]] = "A Corregir" 
                #sendNotify(order["id_origin"])#<<<<Importante
        else:
          #  print(response.status_code)
            sleep(0.5)
            orderChecker(order)
        #financial_status

        return True
    else:
        Resultados[order["_id"]] = "Sin Cambios" 



with open('configs.json') as data:
    companies = json.load(data)
    counter=0
    for company in companies:
        print("Compañia {} Revisando Ordenes".format(counter))
        counter+=1
        app_id          = company["app_id"]
        secret_id       = company["secret_id"]
        redirect_uri    = company["redirect_uri"]
        Resultados      = {}

        conexion =  Centry(app_id , secret_id ,redirect_uri)

        if (conexion.client_credentials()) :
            Company = json.loads(  conexion.CompanyInfo().text)
            Company_name = Company['name']
            Company_id = Company['_id']
            print( "Conectado a : "+ Company_name  )

            init_time = time()
            pedidos =  json.loads( conexion.get_orders({
                "_status":"pending",
                "origin" : "Shopify",
                "created_at_gte":"2020-05-15T00:00:00.000-03:00"
                #,"_id" :"5ecc2f1a3092c1038661ba96"
            }).text)
            MAX_THREADS = 15
            middle_time= time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                executor.map(orderChecker, pedidos)
            end_time= time()
            elapsed = end_time - init_time
            print("Resumen de Ejecución:")
            print("Ordenes A Corregir      : {}".format(     str(list(Resultados.values()).count("A Corregir"))       ))
            print("Ordenes sin cambios    : {}".format(     str(list(Resultados.values()).count("Sin Cambios"))   ))
            print("Ordenes Que Fallaron   : {}".format(     str(list(Resultados.values()).count("Fallo"))         ))
            print("Tiempo de descarga de datos {} segundos.".format( middle_time - init_time))
            print("Tiempo de sincronizacion de datos {} segundos.".format(end_time - middle_time))
            print("Tiempo transcurrido con {} hilos fue {} segundos.".format(MAX_THREADS, elapsed))
            
            with open('log/resultados_{}.json'.format(Company_name),'w') as outfile:
                json.dump(Resultados,outfile)
        else:
            print("No se pudo establecer conexión con Centry.cl")





    
    
   



