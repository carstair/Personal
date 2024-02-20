:local PT1 "PUERTO PRINCIPAL";
:local PT2 "PUERTO RESPALDO";
:local pingTo "GW RED";
:local pingFrom "IP ROUTER";
:local pingCount 5;
:local text [/file get test.txt contents]; ##Se extrae contenido del archivo para ocuparlo en condiciones.

##INICIO CONDICIONAL######
:if ([/ping $pingTo src-address=$pingFrom count=$pingCount] = 0 && ($text = 0)) do={     
/interface bridge port remove [find interface=$PT1]
/interface enable $PT2
:log error message="ENLACE PRINCIPAL DOWN";
/file set test.txt contents=1
} 

##INICIO CONDICIONAL CUANDO LEVANTE LA FIBRA #####
:if ([/ping $pingTo src-address=$pingFrom count=$pingCount] > 3 && ($text = 1)) do={
:log error message="PING FUNCIONA"
/interface disable $PT2
:log error message="DISABLE FUNCIONA"
/interface bridge port add bridge=BRIDGE_ACCESO interface=$PT1
:log error message="ADD BRIDGE FUNCIONA"
/file set test.txt contents=0
}
