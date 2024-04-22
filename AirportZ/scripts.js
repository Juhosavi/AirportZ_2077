'use strict';

//LOAD GAME "nappula" toimivuus
document.getElementById('loadgame').addEventListener('click', async function () {
    const playerName = prompt('Please enter your player name:');
    if (playerName) {
        hideButtons();
        // Haetaan pelaajan tiedot load player funktiosta ja odotetaan awaitilla
        const playerData = await loadPlayer(playerName);
        // Tarkistetaan, onko pelaajan tiedot saatu
        if (playerData && playerData.location) {
            // Keskitetään kartta pelaajan sijaintiin
            haeKaupunki(playerData.location);
        } else {
            console.log('Player not found.');
        }
    }
});
//piilottaa alkubuttonit painettaessa.
function hideButtons() {
    document.getElementById('loadgame').style.display = 'none';
    document.getElementById('newgame').style.display = 'none';
}
async function loadPlayer(playerName) {
    try {
        const url = `http://localhost:3000/loadPlayer?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

//NEW GAME "nappula" toimivuus---KESKEN---menee alkudialogiin mutta ei viellä jatkoa mihin menee sen jälkeen.
document.getElementById('newgame').addEventListener('click', async function () {
    const playerName = prompt('Please enter your new player name:');
    if (playerName) {
        //jos saatu nimi lähetetään se addNewPlayerille ja odoetaan.
        await addNewPlayer(playerName);
        hideButtons();
        displayGameInfo();
        setTimeout(async () => {
            const playerData = await loadPlayer(playerName);
            if (playerData && playerData.location) {
                // Keskitetään kartta pelaajan sijaintiin
                haeKaupunki(playerData.location);
            } else {
                console.log('Player not found.');
            }
            hideGameInfo();
        }, 5000); //  5 sekuntia
    }
});
async function addNewPlayer(playerName) {
    try {
        const url = `http://localhost:3000/addPlayer`;
        const playerData = {name: playerName};

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(playerData)
        });

        const jsonResponse = await response.json();
    } catch (error) {
        console.log(error.message);
    } finally {
        console.log('New player attempt complete');
    }
}

var kartta = L.map('kartta');
var karttaTaso = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(kartta);

function haeKaupunki(location) {
    var url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(location);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                var lat = parseFloat(data[0].lat);
                var lon = parseFloat(data[0].lon);

                // Aseta näkymä ja zoomaustaso
                kartta.setView([lat, lon], 13);

                // Näytä kartta-elementti ja päivitä sen koko
                var karttaElementti = document.getElementById('kartta');
                karttaElementti.style.display = 'block';
                kartta.invalidateSize(); // Kutsu tätä funktiota jos kartta oli aiemmin piilossa

                // Lisää merkki kartalle jos halutaan näyttää tietty paikka
                L.marker([lat, lon]).addTo(kartta)
                    .bindPopup('You are here').openPopup();
            } else {
                alert('Location not found.');
            }
        })
        .catch(error => {
            console.error('Error fetching location data:', error);
        });
}
//Näyttää Pelinalku infot.
function displayGameInfo() {
    const gameInfo = document.getElementById('gameInfo');
    gameInfo.style.display = 'block';
}
//piilottaa pelinalkuinfot.
function hideGameInfo() {
    const gameInfo = document.getElementById('gameInfo');
    gameInfo.style.display = 'none';
}
