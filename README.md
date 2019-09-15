# zabbix-api-query-layer

A Flask (Python) application to simplify data extraction from Zabbix. It is an API that abstracts the ".get()" calls to the Zabbix API.

## Run the application with Docker

sudo docker run -d -p 80:80 --name zql thiagomdiniz/zabbix-api-query-layer

## JSON/Payload structure

to do

## Request examples

### Trigger filter
```
curl -H 'Content-type:application/json' -X POST http://localhost/zabbix -d '
{
  "server":"https://192.168.100.250/zabbix",
  "trigger":{
    "filter":{"triggerids":"15414"}
  }
}' -u YourZabbixUser:YourZabbixPassword
```

Output:
```json
[
    {
        "trigger": [
            {
                "triggerid": "15414",
                "expression": "{16962}<0",
                "description": "DC",
                "url": "",
                "status": "0",
                "value": "0",
                "priority": "0",
                "lastchange": "0",
                "comments": "",
                "error": "",
                "templateid": "0",
                "type": "0",
                "state": "0",
                "flags": "0",
                "recovery_mode": "0",
                "recovery_expression": "",
                "correlation_mode": "0",
                "correlation_tag": "",
                "manual_close": "0",
                "details": ""
            }
        ]
    }
]
```

### More complex request
```
curl -H 'Content-type:application/json' -X POST http://localhost/zabbix -d '
{
   "server":"https://192.168.100.250/zabbix",
   "zabbix-version":"",
   "hostgroup":{
      "pk":"groupid",
      "filter":{},
      "host":{
         "pk":"hostid",
         "fk":"groupids",
         "filter":{"hostids":"10084","output":["hostid","name"]},
         "item":{
            "filter":{"itemids":"23306","output":["itemid","name","key_"]},
            "fk":"hostids"
         }
      }
   },
   "trigger":{
      "filter":{"triggerids":"15414"}
   }
}' -u YourZabbixUser:YourZabbixPassword
```

Output:
```json
[
    {
        "zabbix-version": "4.2.3"
    },
    {
        "hostgroup": [
            {
                "groupid": "1",
                "name": "Templates",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "2",
                "name": "Linux servers",
                "internal": "0",
                "flags": "0",
                "host": [
                    {
                        "hostid": "10084",
                        "name": "Zabbix server",
                        "item": [
                            {
                                "itemid": "23306",
                                "name": "CPU $2 time",
                                "key_": "system.cpu.util[,user]"
                            }
                        ]
                    }
                ]
            },
            {
                "groupid": "4",
                "name": "Zabbix servers",
                "internal": "0",
                "flags": "0",
                "host": [
                    {
                        "hostid": "10084",
                        "name": "Zabbix server",
                        "item": [
                            {
                                "itemid": "23306",
                                "name": "CPU $2 time",
                                "key_": "system.cpu.util[,user]"
                            }
                        ]
                    }
                ]
            },
            {
                "groupid": "5",
                "name": "Discovered hosts",
                "internal": "1",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "6",
                "name": "Virtual machines",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "7",
                "name": "Hypervisors",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "8",
                "name": "Templates/Modules",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "9",
                "name": "Templates/Network Devices",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "10",
                "name": "Templates/Operating Systems",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "11",
                "name": "Templates/Servers Hardware",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "12",
                "name": "Templates/Applications",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "13",
                "name": "Templates/Databases",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "14",
                "name": "Templates/Virtualization",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "15",
                "name": "My Home",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "16",
                "name": "Remote site",
                "internal": "0",
                "flags": "0",
                "host": []
            },
            {
                "groupid": "17",
                "name": "Remote site/Linux",
                "internal": "0",
                "flags": "0",
                "host": []
            }
        ]
    },
    {
        "trigger": [
            {
                "triggerid": "15414",
                "expression": "{16962}<0",
                "description": "DC",
                "url": "",
                "status": "0",
                "value": "0",
                "priority": "0",
                "lastchange": "0",
                "comments": "",
                "error": "",
                "templateid": "0",
                "type": "0",
                "state": "0",
                "flags": "0",
                "recovery_mode": "0",
                "recovery_expression": "",
                "correlation_mode": "0",
                "correlation_tag": "",
                "manual_close": "0",
                "details": ""
            }
        ]
    }
]
```
