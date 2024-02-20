:local pingTo "GW Red de Administración";
:local pingFrom "IP HOST "; 
:local pingCount 5;
:local text [/file get pub/test.txt contents]; #Archivo de texto para condicionales.

:if (([/ping $pingTo src-address=$pingFrom count=$pingCount] = 0) && ($text = 0)) do={
:log error message="ENLACE PRINCIPAL DOWN";
:ip/address/disable numbers=1 #Deshabilita la Publica en el puerto Principal
:ip/address/enable numbers=2  #Habilita la publica en el puerto de respaldo
:log error message="ENLACE BK UP";
/file set pub/test.txt contents=1
} 
:if (([/ping $pingTo src-address=$pingFrom count=$pingCount] > 3) && ($text = 1)) do={
:log info message="ENLACE BK DOWN";
:ip/address/disable numbers=2 #Deshabilita la Publica en el puerto de respaldo
:ip/address/enable numbers=1  #Habilita la publica en el puerto Principal
:log error message="ENLACE PRINCIPAL UP";
/file set pub/test.txt contents=0
}
