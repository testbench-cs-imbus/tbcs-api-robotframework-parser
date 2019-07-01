# Robot Framework Integration für TestBench CS
## Installationanweisung:
Aktuell wird der Wrapper noch von test.pypi.org installiert (sollte als Administrator ausgeführt werden, da sonst ggf. PATH nicht richtig gesetzt wird).

CMD: `pip install --extra-index-url https://test.pypi.org/simple/ tbcs-rf-wrapper`

## Importieren von Robot Tests:
Um Robot-Tests in eine TestBench CS Instanz zu importieren, muss dem Parser eine JSON-Konfigurationsdatei mit folgenden Feldern übergeben werden:
```
{
  "server_address": <my.testbench.instance: String>,                        # z.B. "trynow01-eu.testbench.com"
  "tenant_name": <my.tenant: String>,                                       # z.B. "demouser_xy"
  "product_id": <my.product.id: Int>,                                       # z.B. 3
  "tenant_user": <my.user: String>,                                         # z.B. "demouser_xy"
  "password": <my.password: String>,                                        # z.B. "123456"
  "use_system_proxy": <use.proxy: Boolean>,                                 # z.B. true ## muss genau dann false sein, wenn im System ein Proxy gesetzt ist, der ignoriert werden soll
  "truststore_path": <my.truststore: String>                                # z.B. "/usr/lib/python3/dist-packages/certifi/cacert.pem" ## wird auf Windows ignoriert, Feld muss aber trotzdem vorhanden sein
}
```
Außerdem muss dem Parser das Verzeichnis, in dem sich die zu importierenden Robot-Tests befinden übergeben werden. Der Parser importiert alle Tests, inklusive Testschritte, aus allen .robot-Files in dem gegeben Verzeichnis und allen Unterverzeichnissen.

Nach korrekter Installation können Tests mit folgendem systemweitem Befehl importiert werden:

CMD: `robot-parser <pfad.zu.json.config> <pfad.zu.verzeichnis.mit.robot.tests>`

## Reporten von Testergebnissen:
Um die Testergebnisse eines oder mehrere Robot Tests in die TestBench CS importieren zu können wird ein Listener zur Verfügung gestellt. Wie auch bei anderen Listenern muss die Listener-Klasse beim Starten der Tests als Parameter übergeben werden. Zudem muss dem Listener als Konstruktorparameter der Pfad zu einer JSON-Konfigurationsdatei (wie oben) übergeben werden:

CMD: `robot --listener <pfad.zu.listener.klasse>:"<pfad.zu.json.config>" <pfad.zu.verzeichnis.mit.robot.tests>`

Wenn das Modul global installiert wurde, könnte der Befehl auf einer Linux Umgebung folgendermaßen aussehen:

CMD: `robot --listener /usr/local/lib/python3.6/dist-packages/robot_listener/RobotListener.py:"tbcs.config.json" meineTests/`

Bei Bedarf kann das Installationsverzeichnis über die Python-Shell gefunden werden (Beispiel Ubuntu):
```
user@host:/# python3
Python 3.6.8 (default, Jan 14 2019, 11:02:34) 
[GCC 8.0.1 20180414 (experimental) [trunk revision 259383]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from robot_listener import RobotListener
>>> import sys, os
>>> os.path.abspath(sys.modules[RobotListener.__module__].__file__)
'/usr/local/lib/python3.6/dist-packages/robot_listener/RobotListener.py'
```