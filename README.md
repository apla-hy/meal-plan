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

## Sovelluksen tilanne - välipalautus 2

Sovelluksen keskeisten toimintojen toteutus on aloitettu. Tällä hetkellä seuraavat toiminnot on alustavasti toteutettu:
* Käyttäjähallinta
	* Käyttäjätunnuksen luonti
	* Kirjautuminen
	* Salasanan vaihto
* Aterioiden suunnittelu
	* Aterioiden valinta alasvetovalikoista
	* Samalle päivälle voidaan valita useita aterioita kuten lounas ja päivällinen
* Nimikkeiden ylläpito osittain (uusien nimikkeiden luonti ei ole vielä mahdollista)

Toteutuksessa ei ole vielä keskitytty juuri ollenkaan seuraaviin asioihin:
* Syötettävien tietojen tarkistus ja virheiden käsittely
* Ulkoasu
* Tietoturva

## Sovelluksen testaus

Sovelluksen testaaminen onnistuu [Herokussa](https://ruokasuunnittelu.herokuapp.com/).

Helpointa on käyttää valmiiksi luotua käyttäjätunnusta *user*, jonka salasana on *user*. Sovellukseen voi myös luoda uuden käyttäjätunnuksen ja testata toiminnallisuutta sillä.

