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

## Käyttöohjeet

Kirjautumisen jälkeen sovellus avautuu suunnittelunäkymään. Eri päiville ja aterioille valitaan valmistettava ateria eli resepti. Valintalistalla olevat rivit, joiden lopussa on teksti '(valmis)' tarkoittavat, että aterialla syödään aikaisemmin valmistettua ruokaa. Näitä valintoja ei oteta huomioon ostoslistan luonnissa. Reseptin valinnan sijasta kenttiin voi myös kirjoittaa vapaamuotoisia muistiinpanoja.

Suunnitelunäkymän aikaväliä voi mukauttaa muuttamalla aloituspäivää ja suunnittelujaksoa. Kun suunnitelma on valmis, painamalla napista 'Luo ostoslista', sovellus luo uuden ostoslistan valittujen reseptien perusteella ja näyttää sen. Ostoslistaa voi muokata ja siihen voi lisätä rivejä nimellä tallennetuilta ostoslistoilta.

Valmiin ostoslistan rivejä voi merkitä ostetuiksi painamalla ostoslistan rivin vasemmassa laidassa olevaa merkintänappia.

Ruudun ylälaidan valikosta voi siirtyä ylläpitämään reseptejä, nimikkeitä ja nimikeluokkia. Nimikkeiden muokkaus onnistuu myös ostoslistan ja reseptien rivien oikeassa laidassa olevien muokkausnappien kautta.

## Sovelluksen testaus

Sovelluksen testaaminen onnistuu [Herokussa](https://ruokasuunnittelu.herokuapp.com/).

Helpointa on käyttää valmiiksi luotua käyttäjätunnusta *user1*, jonka salasana on *password1*. Sovellukseen voi myös luoda uuden käyttäjätunnuksen ja testata toiminnallisuutta sillä.

## Sovelluksen tilanne - lopullinen palautus

Suunniteltu toiminnallisuus on toteutettu. Sovelluksessa on kuitenkin myös kehitystarpeita:
* Ulkoasu ja käytettävyys
	* Käytettävyyttä pienellä ruudulla olisi hyvä vielä parantaa
	* Tuki kaikille yleisille laitteille ja selaimille
		* Eri laitteita ja selaimia on testattu jonkin verran mutta ei kattavasti
		* Html datalist ei toimi kuten pitäisi kaikilla mobiiliselaimilla. Esimerkiksi Androidissa Firefox-selaimessa, valintalista ei tule näkyviin mutta Chrome-selaimessa lista toimii.
* Käyttäjähallinta
	* Suunnitelmat ja ostoslistat ovat käyttäjäkohtaisia. Nimikkeet, nimikeluokat ja reseptit ovat yhteisiä. Tämä helpottaa sovelluksen käytön aloitusta eli uuden käyttäjän ei tarvitse luoda tyhjästä nimikeluokkia, nimikkeitä ja reseptejä. Muutokset yhteisiin tietoihin kuitenkin vaikuttavat muiden käyttäjien ympäristöön. Tarkoitus on kehittää käyttäjähallintaa siten, että aloitus on edelleen helppoa mutta tiedot kuitenkin käyttäjäkohtaisia. Aika ei riittänyt tämän toteutukseen kurssin aikana. Osana tätä toteutusta on tarkoitus myös mahdollistaa nimikeluokkien, nimikkeiden ja reseptien poisto tai piilotus.

## Tietokannan rakenne

Tietokannan rakenne selviää tiedostosta [schema.sql](https://github.com/apla-hy/meal-plan/blob/main/schema.sql). Taulussa *plan_rows* seuraavien kenttien käyttötarkoitus on:
* recipe_0: Lounaaksi valittu resepti.
* notes_0: Lounaaksi voi myös valita aikaisemmin valmistetun valmiin ruuan listalta tai kirjoittaa muistiinpanoja. Tällainen valinta tallennetaan tähän kenttään.
* recipe_1: Päivälliseksi valittu resepti.
* notes_1: Päivälliseksi voi myös valita aikaisemmin valmistetun valmiin ruuan listalta tai kirjoittaa muistiinpanoja. Tällainen valinta tallennetaan tähän kenttään.
* recipe_2: Lisäruoka-kohtaan valittu resepti.
* notes_2: Lisäruuaksi voi myös valita aikaisemmin valmistetun valmiin ruuan listalta tai kirjoittaa muistiinpanoja. Tällainen valinta tallennetaan tähän kenttään.


