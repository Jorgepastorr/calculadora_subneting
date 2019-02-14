#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @jorgepastorr
# 11/02/2019
# calculadora subneting

# prog ip cidr num_redes
# ejemplo: python3 calc-subneting.py 192.168.0.0 24 2


import sys
import subneting
import re


if len(sys.argv) != 4 :
    print("Error: número de argumentos incorrecto")
    print("Usage: prog ip cidr num_redes")
    exit(1)


if not ( sys.argv[2].isdigit() and sys.argv[3].isdigit() ):
    print("Error: los argumentos de cidr y num_redes han de ser dígitos natrales")
    print("Usage: prog str(ip) int(cidr) int(num_redes)")
    exit(2)

ip = sys.argv[1]
cidr = int(sys.argv[2])
num_redes = int(sys.argv[3])


patron = '^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$'
if ( re.search( patron, ip) == None ):
    print("Error: la ip ( {ip} ) tiene un formato incorrecto")
    print("Inserta una ip valida en ipv4")
    print("Usage: prog ip cidr num_redes")
    exit(3)


# # ------------- programa ----------------------


# calcular nuevos bits de cidr
bits_necesarios = subneting.bits_para_red(num_redes)
nuevo_cidr = cidr + bits_necesarios

# si cidr + bits necesarios son superiores a 30. demasiadas redes solicitadas
if nuevo_cidr > 30 :
    print("Error: El numero de redes solicitadas, no son posibles")
    print(f"Se necesitarian {nuevo_cidr} bits para red")
    print("Usage: prog ip cidr num_redes")
    exit(4)    


# pasar ip decimal a binaria
ip_bin = subneting.ip_decim_a_bin(ip)

# info red original
inf_red_origin = {}
inf_red_origin["red"] = subneting.datos_red(ip_bin, cidr, cidr, 0, "red")
inf_red_origin["primer_host"] = subneting.datos_red(ip_bin, cidr, cidr, 0, "primer_host")
inf_red_origin["ultimo_host"] = subneting.datos_red(ip_bin, cidr, cidr, 0, "ultimo_host")
inf_red_origin["broadcast"] = subneting.datos_red(ip_bin, cidr, cidr, 0, "broadcast")

# info nuevas redes en binario
redes_binarias = []
for red in range(0,num_redes):
    datos = {}
    datos["red"] = subneting.datos_red(ip_bin, cidr, nuevo_cidr, red, "red")
    datos["primer_host"] = subneting.datos_red(ip_bin, cidr, nuevo_cidr, red, "primer_host")
    datos["ultimo_host"] = subneting.datos_red(ip_bin, cidr, nuevo_cidr, red, "ultimo_host")
    datos["broadcast"] = subneting.datos_red(ip_bin, cidr, nuevo_cidr, red, "broadcast")
    redes_binarias.append( datos )
# print(redes_binarias[0]['red'])

# mascara de la nueva red
mascara = subneting.cidr_a_masc_bin(nuevo_cidr)

# numero de hosts disponibles por red
num_hosts_disponibles = subneting.cird_num_hosts(nuevo_cidr)

# numero de redes disponibles
redes_disponibles = 2 ** bits_necesarios

# total hosts para las redes seleccionadas
num_total_hosts = num_hosts_disponibles * num_redes

# string final
print(f"""
Dirección original: {ip}/{cidr}
Subredes demandadas: {num_redes}
Total hosts: {num_total_hosts}

RED original: 
Network:\t\t {subneting.ip_bin_a_decimal(inf_red_origin['red']):12}/{cidr}\t {inf_red_origin['red']} 
Primer host:\t\t {subneting.ip_bin_a_decimal(inf_red_origin['primer_host']):15}\t {inf_red_origin['primer_host']}
Ultimo host:\t\t {subneting.ip_bin_a_decimal(inf_red_origin['ultimo_host']):15}\t {inf_red_origin['ultimo_host']}
Broadcast:\t\t {subneting.ip_bin_a_decimal(inf_red_origin['broadcast']):15}\t {inf_red_origin['broadcast']}

    Mascara nueva red:\t {subneting.ip_bin_a_decimal(mascara):15}\t {mascara}
""")

for i in range(0, num_redes):
    print(f"""
    RED: {i}
    Network:\t\t {subneting.ip_bin_a_decimal(redes_binarias[i]['red']):12}/{nuevo_cidr}\t {redes_binarias[i]['red']} 
    Primer host:\t {subneting.ip_bin_a_decimal(redes_binarias[i]['primer_host']):15}\t {redes_binarias[i]['primer_host']}
    Ultimo host:\t {subneting.ip_bin_a_decimal(redes_binarias[i]['ultimo_host']):15}\t {redes_binarias[i]['ultimo_host']}
    Broadcast:\t\t {subneting.ip_bin_a_decimal(redes_binarias[i]['broadcast']):15}\t {redes_binarias[i]['broadcast']}
    Hosts disponibles: {num_hosts_disponibles}
    """)
print(f"Subnets disponibles: {redes_disponibles}")


# ----------------------------------------