:local text [/file get pub/test.txt contents];
interface/ethernet/monitor ether3 once do={:if (($"status" = "no-link") && ($text = "0")) do={
:log info "ether1 is down"
:ip/address/enable numbers=2
:ip/address/disable numbers=1
/file set pub/test.txt contents=1
} 
:if (($"status" = "link-ok") && ($text = "1")) do={
:log info "ether1 is up"
:ip/address/enable numbers=2
:ip/address/disable numbers=1
/file set pub/test.txt contents=0
} 
}