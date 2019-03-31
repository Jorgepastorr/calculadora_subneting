#!/usr/bin/python3
# @jorgepastorr
# 10/02/2019
# creando funciones para calculadora ip


# ------------- trato de octetos e ip's -----------------------------
def decimal_a_bin(num):
    """
    F. que convierte una cadena de decimal a binario
    decimal_a_bin( int )
    return str
    """
    binario=""
    if num == 0:
        binario = "0"

    while num > 0:
        binario = str(num % 2 ) + binario
        num //= 2
    
    return f"{int(binario):08}"


def binario_a_decimal(binario):
    """
    F. convierte de binario a decimal
    binario_a_decimal( str(binario) )
    return int
    """
    decimal = 0
    potencia = 0
    for bit in binario[::-1]:
        decimal += int(bit) * 2 ** potencia
        potencia += 1

    return decimal

def ip_decim_a_bin(ip_dec):
    """
    F. convierte ip decimal a binaria separando octetos por .
    Formato: octeto.octeto.octeto.octeto
    ip_decim_a_bin( str(ip_dec) )
    return str
    """
    ip_bin = "" 
    for oct_dec in ip_dec.split('.'):
        ip_bin += decimal_a_bin( int(oct_dec) ) + "."
    
    return ip_bin[:-1]

def ip_bin_a_decimal(ip_bin):
    """
    F. convierte ip binaria a decimal separando octetos por .
    Formato: octeto.octeto.octeto.octeto
    ip_decim_a_bin( str(ip_bin) )
    return str
    """
    ip_dec = ""
    for oct_bin in ip_bin.split('.'):
        ip_dec += str( binario_a_decimal(oct_bin) ) + "."
    
    return ip_dec[:-1]

# ----------------------------- trato de mascaras --------------------------------

def cidr_a_masc_bin(num_cidr):
    """
    F. convierte numero cidr en mascara binaria
    cidr_a_bin( int(num_cidr) )
    return str(mascara)
    """
    bits_host = 32 - num_cidr
    mascara_sin_corte = "1" * num_cidr + "0" * bits_host
    mascara = anyado_formato(mascara_sin_corte)

    return mascara

def anyado_formato(mascara_sin_corte):
    """
    F. dada una mascara de bits sin formato añade . de formatos
    octeto.octeto.octeto.octeto
    anyado_formato( str(mascara_sin_corte) )
    return str
    """
    mascara = ""
    for corte in ( 0,8,16,24):
        mascara += mascara_sin_corte[corte:corte+8] + "."

    return mascara[:-1]


def cird_num_hosts(num_cidr):
    """
    F. retorna numero de hosts que son posibles asignar con ese cidr
    cird_num_hosts( int(num_cidr) )
    return int
    """
    bits_host = 32 - num_cidr
    return  2 ** bits_host - 2


def masc_bin_a_cidr(masc_bin):
    """
    F. convierte mascara binaria en numero de cird
    Formato: octeto.octeto.octeto.octeto
    masc_bin_a_cidr( str(masc_bin) )
    return int
    """
    cidr = 0
    for octeto in masc_bin.split('.'):
        for bit in octeto:
            if bit == "1":
                cidr += 1
    
    return cidr



def bits_para_red(num_redes, host=None):
    """
    F. dado un numero de redes calcula el numero de bits que necesita para dichas redes
    num_redes: numero de redes 
    host: por defecto None, si se activa con True, num_redes se convierte en bits, \
        calcula numero de hosts permitidos con dichos bits.

    bits_para_red( int(num_redes), opcional True )
    return int
    """
    redes_no_permitidas = 0
    if host == True:
        redes_no_permitidas = 2

    bits = 0
    while num_redes > ( 2 **  bits - redes_no_permitidas ):
        bits += 1
        
    return bits 

# ----------------- trato de redes -------------------------

def datos_red(ip_binaria, cidr_red, cidr_subred, red_num, dato):
    """
    F. extrae datos de la nueva red de subneting
    datos_red( str(ip_binaria), int(cidr_red), int(cidr_subred), int(red_num), str(dato) )
    ip_binaria: ip binaria en formato x.x.x.x
    cidr_red: cidr red original
    cidr_subred: cird de la subred
    red_num: nmero de red a la que extraer datos 0-?
    dato: dato que extraer opciones: ( red, primer_host, ultimo_host, broadcast )
    return str
    """

    # quito formato
    ip_sin_formato = ip_binaria.replace('.','')

    # crear corte con primer cidr
    red = ip_sin_formato[:cidr_red]
    
    # inserto red desde el corte
    bits_necesarios = cidr_subred - cidr_red 
    if bits_necesarios > 0  :
        
        red += f"{int(decimal_a_bin(red_num)):0{bits_necesarios}}"

    # rellenar al gusto segun dato
    if dato == "red":
        red += "0" * ( 32 - cidr_subred )
    elif dato == "broadcast":
        red += "1" * ( 32 - cidr_subred )
    elif dato == "primer_host":
        red += "0" * ( 32 - ( cidr_subred  + 1 ) ) + "1"
    elif dato == "ultimo_host":
        red += "1" * ( 32 - ( cidr_subred + 1 ) ) + "0" 

    nueva_red = anyado_formato(red)

    return nueva_red 
    
