# ZQL -> zabbix-api-query-layer

ZQL is a Flask (Python) application to simplify data extraction from Zabbix. It is an API that abstracts the ".get" calls to the Zabbix API and allows you to make multiple requests to the Zabbix API with just one request.

## Run the application with Docker

sudo docker run -d -p 80:80 --name zql thiagomdiniz/zabbix-api-query-layer

## Endpoints

* GET /health

Returns http 200 code and a JSON message stating that it is alive.

* POST /zabbix

Requires Basic Auth and a JSON Payload.

Basic Auth is the -u parameter of the curl command or the Authorization header of the http request.

ZQL will use the username and password entered in Basic Auth to authenticate to the Zabbix API.

## JSON/Payload structure - How it works

In ZQL endpoint /zabbix you can submit a query JSON using Zabbix API methods that have ".get":

![zql1](/readme_images/zql1.png)

SQL allows you to perform nested queries using "pk" (primary key) and "fk" (foreign key) to filter subqueries based on the return of the previous query.

For example, for the host group object the unique identifier / primary key is the "groupid" field:

![zql1](/readme_images/zql3.png)

And to filter a host object on each hostgroup, the "groupids" field is the foreign key, where we will put the value of the "groupid" primary key:

![zql1](/readme_images/zql2.png)

We will take the payload below as an example:

![zql1](/readme_images/zql4.png)

* 1) "server" is a required field. should contain your Zabbix frontend address;

* 2) "zabbix-version" is a optional field. When used adds to the response the version of Zabbix queried;

* 3) Is the name of the Zabbix API method that contains the ".get" query;

* 4) "filter" is a required field. Create filter based on Python zabbix-api library. Use {} for empty filter;

* 5) "pk" is a required field only when the query has subqueries. Is the ID / primary key of the object;

* 6) "fk" is a required field only for subqueries. Is the field that will be added to the subquery filter with the ID / primary key value of the parent query result.

## Request examples

### Health status
```
curl -H 'Content-type:application/json' http://localhost/health
```

Output:
```json
{
    "message": "alive"
}
```

### Trigger filter
```
curl -H 'Content-type:application/json' -X POST http://localhost/zabbix -d '
{
  "server":"https://192.168.100.250/zabbix",
  "trigger":{
    "filter":{"triggerids":"15414","output":["triggerid","description"]}
  },
  "host":{
	"filter":{"hostids":"10084","output":["hostid","name"]}
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
                "description": "DC"
            }
        ]
    },
    {
        "host": [
            {
                "hostid": "10084",
                "name": "Zabbix server"
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

