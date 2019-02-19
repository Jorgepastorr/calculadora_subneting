#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @jorgepastorr
# 13/02/2019
# calculadora vlsm

# prog -i ip -c cidr -n num_redes

import argparse
import subneting
import re

texto_descripcion = """
Calculadora de subneting ( vlsm ), calcula a partir de los hosts demandados las posible redes.
( No tiene control de errores si te pasas en numero de hosts )
"""


# analizador = argparse.ArgumentParser(description=texto_descripcion)
analizador = argparse.ArgumentParser(prog="calc-vlsm.py",
                                    usage="%(prog)s -i str(ip) -c int(cidr) -r int(num_redes[...])",
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description=texto_descripcion)
analizador.add_argument("-i","--ip", help="ip de red de donde partir a calcular redes, en formato decimal", required=True)
analizador.add_argument("-c","--cidr", help="cidr de la ip de red base", type=int, required=True)
analizador.add_argument("-n","--hosts", help="numero de hosts que se desean por red", required=True, nargs="*", type=int)

argumento = analizador.parse_args()


patron = '^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$'
ip = argumento.ip
if ( re.search( patron, ip) == None ):
    print(f"Error: la ip ( {ip} ) tiene un formato incorrecto")
    print("Inserta una ip valida en ipv4")
    print("Ej formato: 192.168.0.0")
    print("Usage: prog -i st(ip) -c int(cidr) -r int(num_redes[...])")
    exit(1)

cidr = argumento.cidr
hosts = argumento.hosts

if not argumento.hosts:
    print("Error: el argumento -n esta vacio")
    print("tiene que indicar el numero de hosts que se desean por red")
    print("Usage: prog -i st(ip) -c int(cidr) -r int(num_redes[...])")
    exit(2)



# -----------------  Programa ----------------


# Ordeno los hosts de mayor a menor para poder hacer vlsm
redes_ordenadas = sorted(hosts, reverse=True)

# Añado primera información de las redes
info_redes=[]
numero_de_red = 0
cidr_red_anterior = 0

# Calculo cidr de cada red, desde los hosts demandados
# aprovecho para añadir: hosts por red y masara de red
for host in redes_ordenadas:
    datos_host = {}
    datos_host['cidr'] = 32 - subneting.bits_para_red(host, True)
    datos_host['mascara'] = subneting.cidr_a_masc_bin(datos_host['cidr'])
    datos_host['num_hosts'] = subneting.cird_num_hosts( datos_host['cidr'] )

    # asigno posicion de numero de red, dentro de cada red
    if datos_host['cidr'] == cidr_red_anterior:
        numero_de_red += 1
    else:
        numero_de_red = 0
    
    datos_host['num_red'] = numero_de_red
    info_redes.append( datos_host )

    cidr_red_anterior = datos_host['cidr']
 

# pasar ip a binaria
ip_bin = subneting.ip_decim_a_bin(ip)

# saber cuantas vueltas tiene que dar por red ( cada vez que cabia de cird )
red_anterior = -5
num_vueltas = 0
lista_vueltas_por_red = []

for i in range(0,len(info_redes)):
    
    if info_redes[i]['num_red'] == 0 and red_anterior == 0:
        lista_vueltas_por_red.append(num_vueltas)
        num_vueltas = 0
    elif info_redes[i]['num_red'] == 0 and red_anterior > 0:
        lista_vueltas_por_red.append(num_vueltas)
        num_vueltas = 0
    
    red_anterior = info_redes[i]['num_red']
    num_vueltas += 1

lista_vueltas_por_red.append(num_vueltas)


# Completo los datos de cada red con los datos en binarios 
red_base = ip_bin
cidr_red_anterior = cidr
posicion_red = 0

for vuelta_final in lista_vueltas_por_red:
    for red in range(0,vuelta_final + 1):

        if red == vuelta_final:
            red_base = subneting.datos_red(red_base, cidr_red_anterior, info_redes[posicion_red -1]['cidr'], red, "red")
            cidr_red_anterior = info_redes[posicion_red-1]['cidr']
        else:
            cidr_red_actual = info_redes[posicion_red]['cidr']
            info_redes[posicion_red]["red"] = subneting.datos_red(red_base, cidr_red_anterior, cidr_red_actual, red, "red")
            info_redes[posicion_red]["primer_host"] = subneting.datos_red(red_base, cidr_red_anterior, cidr_red_actual, red, "primer_host")
            info_redes[posicion_red]["ultimo_host"] = subneting.datos_red(red_base, cidr_red_anterior, cidr_red_actual, red, "ultimo_host")
            info_redes[posicion_red]["broadcast"] = subneting.datos_red(red_base, cidr_red_anterior, cidr_red_actual, red, "broadcast")
            posicion_red += 1



# Muestra de datos 

# for i in info_redes:
#     print(i)      

cont = 1
for red in info_redes:
    print(f"""
    RED: {cont}
    Mascara: de red:\t {subneting.ip_bin_a_decimal(red['mascara']):15}\t {red['mascara']}  
    Network:\t\t {subneting.ip_bin_a_decimal(red['red']):12}/{red['cidr']}\t {red['red']} 
    Primer host:\t {subneting.ip_bin_a_decimal(red['primer_host']):15}\t {red['primer_host']}
    Ultimo host:\t {subneting.ip_bin_a_decimal(red['ultimo_host']):15}\t {red['ultimo_host']}
    Broadcast:\t\t {subneting.ip_bin_a_decimal(red['broadcast']):15}\t {red['broadcast']}
    Hosts disponibles: {red['num_hosts']}
    """)
    cont += 1