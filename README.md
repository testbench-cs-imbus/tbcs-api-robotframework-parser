**Installationanweisung:**

Aktuell wird der Wrapper noch von test.pypi.org installiert (sollte als Administrator ausgeführt werden, da sonst ggf. PATH nicht richtig gesetzt wird).

CMD: `python -m pip install --extra-index-url https://test.pypi.org/simple/ tbcs-rf-wrapper`

**Importieren von Robot-Tests:**

Um Robot-Tests in eine TestBench CS Instanz zu importieren, muss dem Parser eine JSON-Konfigurationsdatei mit folgenden Feldern übergeben werden:

```
{
  "server_address": <my.testbench.instance: String>,                        # z.B. "trynow01-eu.testbench.com"
  "tenant_name": <my.tenant: String>,                                       # z.B. "demouser_xy"
  "product_id": <my.product.id: Int>,                                       # z.B. 3
  "tenant_user": <my.user: String>,                                         # z.B. "demouser_xy"
  "password": <my.password: String>,                                        # z.B. "123456"
  "use_system_proxy": <use.proxy: Boolean>,                                 # z.B. true ## muss genau dann true sein, wenn im System ein Proxy gesetzt ist, der ignoriert werden soll
  "truststore_path": <my.truststore: String>                                # z.B. "/usr/lib/python3/dist-packages/certifi/cacert.pem" ## wird auf Windows ignoriert, Feld muss aber trotzdem vorhanden sein
}
```

Außerdem muss dem Parser das Verzeichnis, in dem sich die zu importierenden Robot-Tests befinden übergeben werden. Der Parser importiert alle Tests, inklusive Testschritte, aus allen .robot-Files in dem gegeben Verzeichnis und allen Unterverzeichnissen.

Nach korrekter Installation können Tests mit folgendem systemweiten Befehl importiert werden:

CMD: `robot-parser <pfad.zu.json.config> <pfad.zu.verzeichnis.mit.robot.tests>`