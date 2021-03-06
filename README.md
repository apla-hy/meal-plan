# Ruokasuunnittelu

Tämä sovellus on toteutettu Helsingin yliopiston aineopintojen *Tietokantasovellus* harjoitustyönä (TKT20011).

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
	* Jokaiselle päivälle voi myös kirjoittaa muistiinpanoja
* Ostoslistan luonti suunnitelman perusteella
	* Ostettavien tuotteiden järjestys siten, että kaupassa kerääminen tai verkkokaupassa tilaaminen onnistuu helposti
	* Usein ostettavien tuotteiden lisääminen listalle helposti 
* Reseptien ylläpito
* Nimikkeiden ylläpito

## Sovelluksen tilanne - lopullinen palautus

Suunniteltu toiminnallisuus on toteutettu. Sovelluksessa on kuitenkin myös kehitystarpeita:
* Ulkoasu ja käytettävyys
	* Ulkoasu ei ole erityisen hyvä, koska sitä ei ollut aikaa viimeistellä
	* Käytettävyys pienellä ruudulla ei ole erityisen hyvä
	* Tuki kaikille yleisille laitteille ja selaimille
		* Eri laitteita ja selaimia on testattu jonkin verran mutta ei kattavasti
		* Html datalist ei toimi kuten pitäisi kaikilla mobiiliselaimilla. Esimerkiksi Androidissa Firefox-selaimessa, lista ei tule näkyviin mutta Chrome-selaimessa lista tulee näkyviin.
* Käyttäjähallinta
	* Suunnitelmat ja ostoslistat ovat käyttäjäkohtaisia. Nimikkeet, luokat ja reseptit ovat yhteisiä. Tämä helpottaa sovelluksen käytön aloitusta eli uuden käyttäjän ei tarvitse luoda tyhjästä nimikeluokkia, nimikkeitä ja reseptejä. Muutokset yhteisiin tietoihin kuitenkin vaikuttavat muiden käyttäjien ympäristöön. Tarkoitus on kehittää käyttäjähallintaa siten, että aloitus on helppoa mutta tiedot kuitenkin käyttäjäkohtaisia. Aika ei riittänyt tämän toteutukseen kurssin aikana. Osana tätä toteutusta on tarkoitus myös mahdollistaa nimikeluokkien, nimikkeiden ja reseptien poisto/piilotus.

## Sovelluksen testaus

Sovelluksen testaaminen onnistuu [Herokussa](https://ruokasuunnittelu.herokuapp.com/).

Helpointa on käyttää valmiiksi luotua käyttäjätunnusta *user*, jonka salasana on *user*. Sovellukseen voi myös luoda uuden käyttäjätunnuksen ja testata toiminnallisuutta sillä.

## Tietokannan rakenne

Tietokannan rakenne selviää tiedostosta [schema.sql](https://github.com/apla-hy/meal-plan/blob/main/schema.sql). Taulussa *plan_rows* seuraavien kenttien käyttötarkoitus on:
* recipe_0: Lounaaksi valittu resepti.
* notes_0: Lounaaksi voi myös valita aikaisemmin valmistetun valmiin ruuan listalta tai kirjoittaa muistiinpanoja. Tällainen valinta tallennetaan tähän kenttään.
* recipe_1: Päivälliseksi valittu resepti.
* notes_1: Päivälliseksi voi myös valita aikaisemmin valmistetun valmiin ruuan listalta tai kirjoittaa muistiinpanoja. Tällainen valinta tallennetaan tähän kenttään.
* recipe_2: Lisäruoka-kohtaan valittu resepti.
* notes_2: Lisäruuaksi voi myös valita aikaisemmin valmistetun valmiin ruuan listalta tai kirjoittaa muistiinpanoja. Tällainen valinta tallennetaan tähän kenttään.


