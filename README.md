En premier lieu, pour télécharger SUMO (gratuit et open-source) : https://eclipse.dev/sumo/

Pour lancer une simulation et visualiser les résultats, il faut d'abord vérifier que les bons fichiers sont présents dans le fichier configuration.sumocfg.
Pour le Scénario 1 :

<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <input>
    <net-file value="Map_Smartseille.net.xml" />
    <route-files value="flows_vf_sorted_by_departure.rou.xml" />
    <additional-files value="parkings.xml" />
  </input>
  <time>
    <begin value="0" />
    <end value="7200" />
  </time>
  <output>
    <!-- Collect vehicle trip information -->
    <tripinfo-output value="tripinfo.xml"/>
    <!-- Collect emissions data -->
    <emission-output value="emissions.xml"/>
  </output>
</configuration>

Pour le scénario 2 : 

<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <input>
    <net-file value="Map_Smartseille.net.xml" />
    <route-files value="flows_s2_updated.rou.xml" />
    <additional-files value="parkings_parking1.add.xml" />
  </input>
  <time>
    <begin value="0" />
    <end value="7200" />
  </time>
  <output>
    <!-- Collect vehicle trip information -->
    <tripinfo-output value="tripinfo.xml"/>
    <!-- Collect emissions data -->
    <emission-output value="emissions.xml"/>
  </output>
</configuration>
  
Puis il suffit d'utiliser cette commande python pour le scénario 1 :
  python script.py
Ou pour le scénario 2 : 
  python script_scenario2_updated.py
