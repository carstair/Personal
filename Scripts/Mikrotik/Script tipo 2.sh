:local PT2 "ether1"; #Enlace de respaldo Radio troncal
:local VLAN1 "vlan#"; #Variable para enlace en SFP
:local VLAN2 "vlan#"; #Variable para enlace en SFP
:local VLAN3 "vlan#"; #Variable para enlace en SFP
:local VLANBK1 "vlan_bk_#"; #Variable para enlace en respaldo de Radio Troncal
:local VLANBK2 "vlan_bk_#"; #Variable para enlace en Radio Troncal
:local VLANBK3 "vlan_bk_#"; #Variable para enlace en Radio Troncal
:local pingTo "GW RED DE ADMINISTRACIÓN";
:local pingFrom "IP HOST DE VLAN ADMINISTRACIÓN"; ##vlan administración
:local pingCount 5;
:local text [/file get flash/test.txt contents]; ##Archivo para condicionales

:if (([/ping $pingTo src-address=$pingFrom count=$pingCount] = 0) && ($text = 0)) do={
/interface disable $VLAN1  #Desactivar VLAN1
/interface disable $VLAN2  #Desactivar VLAN2
/interface disable $VLAN3  #Desactivar VLAN3
/interface enable $PT2     #Habilitar puerto de resplado
/interface enable $VLANBK1 #Habilitar VLAN 1 en BK
/interface enable $VLANBK2 #Habilitar VLAN 2 en BK
/interface enable $VLANBK3 #Habilitar VLAN 3 en BK
:log error message="ENLACE PRINCIPAL DOWN";
/file set flash/test.txt contents=1  ###Texto en 1 condicional de respaldo
} 
:if (([/ping $pingTo src-address=$pingFrom count=$pingCount] > 3) && ($text = 1)) do={
/interface disable $PT2
/interface disable $VLANBK1 #Deshabilitar VLAN 1 en BK
/interface disable $VLANBK2 #Deshabilitar VLAN 3 en BK
/interface disable $VLANBK3 #Deshabilitar VLAN 4 en BK
/interface enable $VLAN1   #Habilitar VLAN 1
/interface enable $VLAN2   #Habilitar VLAN 2
/interface enable $VLAN3   #Habilitar VLAN 3
:log info message="ENLACE PRINCIPAL UP";
/file set flash/test.txt contents=0  #texto 0 condicional de Principal
}
