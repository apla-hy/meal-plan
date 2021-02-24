# Ruokasuunnittelu

Tämä sovellus toteutetaan Helsingin yliopiston aineopintojen *Tietokantasovellus* harjoitustyönä (TKT20011).

## Sovelluksen toiminnallisuus

Sovelluksella voi suunnitella kotona valmistettavat ateriat haluamalleen aikavälille esimerkiksi yhden viikon ajaksi. Suunnitelman perusteella on mahdollista luoda ostoslista ruokakauppaan.

Sovelluksen keskeiset toiminnallisuudet ovat:
* Käyttäjähallinta
	* Käyttäjätunnuksen luonti
	* Kirjautuminen
	* Salasanan vaihto
* Aterioiden suunnittelu
	* Aterioiden valinta alasvetovalikoista
	* Samalle päivälle voidaan valita useita aterioita kuten lounas ja päivällinen
* Ostoslistan luonti suunnitelman perusteella
	* Ostettavien tuotteiden järjestys siten, että kaupassa kerääminen tai verkkokaupassa tilaaminen onnistuu helposti
	* Usein ostettavien tuotteiden lisääminen listalle helposti 
* Reseptien ylläpito
* Nimikkeiden ylläpito

## Sovelluksen tilanne - välipalautus 3

Suurin osa sovelluksen toiminnoista on toteutettu. Tällä hetkellä seuraavat toiminnot puuttuvat:
* Ostettavien tuotteiden järjestys siten, että kaupassa kerääminen tai verkkokaupassa tilaaminen onnistuu helposti
* Usein ostettavien tuotteiden lisääminen listalle helposti

Lisäksi välipalautuksen jälkeen on tarkoitus vielä keskittyä seuraaviin asioihin:
* Syötettävien tietojen tarkistus ja virheiden käsittely kaikissa toiminnoissa
* Ulkoasu
* Tietoturva

## Sovelluksen testaus

Sovelluksen testaaminen onnistuu [Herokussa](https://ruokasuunnittelu.herokuapp.com/).

Helpointa on käyttää valmiiksi luotua käyttäjätunnusta *user*, jonka salasana on *user*. Sovellukseen voi myös luoda uuden käyttäjätunnuksen ja testata toiminnallisuutta sillä.

