:local pingTo "IP GW";
:local pingFrom "IP Host";
:local pingCount 5;
:local text [/file get pub/test.txt contents];
:if ([ping $pingTo src-address=$pingFrom count=$pingCount] = 5 && ($text=1)) do={
/tool/e-mail/send to=user@domain.com cc=user@domain.com subject=asunto body=texto
}