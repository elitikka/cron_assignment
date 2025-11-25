# Tehtävänanto:
Käytä hyväksi aiemmin luotua LEMP-stack arkkitehtuuria ja Streamlit-sovellusta.Tarkista Nginx serverin reverse proxy asetukset niin, että tehty Streamlit-sovellus ohjautuu näkyväksi http://sinun-vps-ip-osoite/data-analysis sivulle. 
Tässä tehtävässa harjoitellaan cronin käyttöä ja eri skriptien tekoa sekä tietokannan käyttöä Linuxissa. 
Muista huolehtia, että palvelut pysyvät käynnissä ja tarvittavat portit ovat auki.

Oheisen ohjeen lisäksi:
- Käytä Githubia versionhallintaan mutta älä jaa API-avaimiasi julkiseen repoon.
- Älä lisää nimeäsi sivulle, jos haluat pysyä anonyymina vertaiselle. Palauta URL:it sivullesi ja Github-repoon (Pidä repo julkisena)

Pisteytys:
- Streamlit-sovellus toimii ohjeistuksen mukaan ja kerryttää ja päivittää dataa 15min välein +6p
- Lisäksi jotain muuta APIa kuin ohjeessa mainittua on käytetty +2p

# Tehtävän toteutus:
- Streamlit-sovellus kerryttää ja päivittää dataa 15min välein osoitteessa http://86.50.23.96/cron_assignment/
- Käytetty Open Weather APIa (ohjeessa mainittu) ja Norjan ilmatieteenlaitoksen APIa
