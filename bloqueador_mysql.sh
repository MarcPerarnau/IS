#!/bin/bash

# CONFIGURACIÓN MYSQL
MYSQL_USER="superiron"
MYSQL_PASS="]zIiZHz-Hq8eHR2h"
MYSQL_DB="ironshield"
MYSQL_HOST="localhost"

# Nombre de la cadena personalizada
CHAIN="BLOQUEOS"

# Crear cadena si no existe
iptables -N $CHAIN 2>/dev/null
iptables -D INPUT -j $CHAIN 2>/dev/null
iptables -I INPUT -j $CHAIN

# Limpia reglas antiguas
iptables -F $CHAIN

# Bloqueo de IPs directamente
mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -h "$MYSQL_HOST" "$MYSQL_DB" -Bse \
"SELECT valor FROM blacklist WHERE tipo='ip';" | while read ip; do
    echo "Bloqueando IP: $ip"
    iptables -A $CHAIN -s "$ip" -j DROP
done

# Bloqueo de dominios (resolviendo IPs)
mysql -u "$MYSQL_USER" -p"$MYSQL_PASS" -h "$MYSQL_HOST" "$MYSQL_DB" -Bse \
"SELECT valor FROM blacklist WHERE tipo='dominio';" | while read domain; do
    ip=$(dig +short "$domain" | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' | head -n 1)
    if [ -n "$ip" ]; then
        echo "Bloqueando dominio $domain (resuelto a $ip)"
        iptables -A $CHAIN -s "$ip" -j DROP
    fi
done
