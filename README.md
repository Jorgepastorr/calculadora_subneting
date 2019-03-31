# Calculadoras subneting y vlsm

## Subneting

Script que pasados los argumentos de una ip de red, su cidr y las redes que quieres añadir calcula sus datos.  

```bash
debian  ➜  python3 calc-subneting.py 192.168.0.0 24 2                  

Dirección original: 192.168.0.0/24
Subredes demandadas: 2
Total hosts: 252

RED original: 
Network:         192.168.0.0 /24     11000000.10101000.00000000.00000000 
Primer host:         192.168.0.1         11000000.10101000.00000000.00000001
Ultimo host:         192.168.0.254       11000000.10101000.00000000.11111110
Broadcast:         192.168.0.255       11000000.10101000.00000000.11111111

    Mascara nueva red:     255.255.255.128     11111111.11111111.11111111.10000000


    RED: 0
    Network:         192.168.0.0 /25     11000000.10101000.00000000.00000000 
    Primer host:     192.168.0.1         11000000.10101000.00000000.00000001
    Ultimo host:     192.168.0.126       11000000.10101000.00000000.01111110
    Broadcast:         192.168.0.127       11000000.10101000.00000000.01111111
    Hosts disponibles: 126


    RED: 1
    Network:         192.168.0.128/25     11000000.10101000.00000000.10000000 
    Primer host:     192.168.0.129       11000000.10101000.00000000.10000001
    Ultimo host:     192.168.0.254       11000000.10101000.00000000.11111110
    Broadcast:         192.168.0.255       11000000.10101000.00000000.11111111
    Hosts disponibles: 126

Subnets disponibles: 2
```

## vlsm

Dada una ip de red, su cidr y los numero de hosts por cada red calcula los datos de cada red.  

### Método de uso

- `-h -help` ayuda del comando
- `-i --ip`  ip de red base de donde partir
- `-c --cidr` cidr de la ip base 
- `-n --hosts` numero de hosts por red

  > Los argumentos -i, -c, -n son obligatorios para la ejecución del script.  

**Ejemplo:**  

```bash
debian  ➜  python3 calc-vlsm.py -i 10.64.0.0 -c 10 -n 4000 1500 300 2 2  

    RED: 1
    Mascara: de red:     255.255.240.0       11111111.11111111.11110000.00000000  
    Network:         10.64.0.0   /20     00001010.01000000.00000000.00000000 
    Primer host:     10.64.0.1           00001010.01000000.00000000.00000001
    Ultimo host:     10.64.15.254        00001010.01000000.00001111.11111110
    Broadcast:         10.64.15.255        00001010.01000000.00001111.11111111
    Hosts disponibles: 4094


    RED: 2
    Mascara: de red:     255.255.248.0       11111111.11111111.11111000.00000000  
    Network:         10.64.16.0  /21     00001010.01000000.00010000.00000000 
    Primer host:     10.64.16.1          00001010.01000000.00010000.00000001
    Ultimo host:     10.64.23.254        00001010.01000000.00010111.11111110
    Broadcast:         10.64.23.255        00001010.01000000.00010111.11111111
    Hosts disponibles: 2046


    RED: 3
    Mascara: de red:     255.255.254.0       11111111.11111111.11111110.00000000  
    Network:         10.64.24.0  /23     00001010.01000000.00011000.00000000 
    Primer host:     10.64.24.1          00001010.01000000.00011000.00000001
    Ultimo host:     10.64.25.254        00001010.01000000.00011001.11111110
    Broadcast:         10.64.25.255        00001010.01000000.00011001.11111111
    Hosts disponibles: 510


    RED: 4
    Mascara: de red:     255.255.255.252     11111111.11111111.11111111.11111100  
    Network:         10.64.26.0  /30     00001010.01000000.00011010.00000000 
    Primer host:     10.64.26.1          00001010.01000000.00011010.00000001
    Ultimo host:     10.64.26.2          00001010.01000000.00011010.00000010
    Broadcast:         10.64.26.3          00001010.01000000.00011010.00000011
    Hosts disponibles: 2


    RED: 5
    Mascara: de red:     255.255.255.252     11111111.11111111.11111111.11111100  
    Network:         10.64.26.4  /30     00001010.01000000.00011010.00000100 
    Primer host:     10.64.26.5          00001010.01000000.00011010.00000101
    Ultimo host:     10.64.26.6          00001010.01000000.00011010.00000110
    Broadcast:         10.64.26.7          00001010.01000000.00011010.00000111
    Hosts disponibles: 2
```

- En este ejemplo se ve como partiendo de una ip de red 10.64.0.0/10, creamos 5 redes que pueden alojar los n hosts indicados 4000,1500,300,2,2.
