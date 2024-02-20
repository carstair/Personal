:local pingTo "190.181.131.113";
:local pingFrom "190.181.131.117";
:local pingCount 5;
:local text [/file get pub/test.txt contents];
:if ([ping $pingTo src-address=$pingFrom count=$pingCount] = 5 && ($text=1)) do={
/tool/e-mail/send to=asuazo@yotateam.com.ni cc=jeperez@yotateam.com.ni subject=FibraCaida body=PRUEBAMK
}