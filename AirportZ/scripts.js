'use strict';
var playerName;
var playerData = null;
var playerStats = null;

//piilottaa alussa "action" nappulat heti.
document.getElementById('travel').style.display = 'none';
document.getElementById('search').style.display = 'none';
document.getElementById('bandage').style.display = 'none';
hide_player_stats();

//LOAD GAME "nappula" kuuntelija clickkauksesta
document.getElementById('loadgame').addEventListener('click', load_game_button)
//LOAD GAME BUTTON
async function load_game_button() {
    playerName = prompt('Please enter your player name:');
    if (playerName) {
        hideButtons();
        // Haetaan pelaajan tiedot load player funktiosta ja odotetaan awaitilla
        playerData = await loadPlayer(playerName);
        // Tarkistetaan, onko pelaajan tiedot saatu
        if (playerData && playerData.location) {
            // Keskitetään kartta pelaajan sijaintiin
            haeKaupunki(playerData.location);
            //näyttää action buttonit
            show_action_buttons();
            await display_player_stats(playerName)
            await fetchFarthestAirport(playerData.location);
        } else {
            console.log('Player not found.');
        }
    }
}
//Tuo näkyviin action buttonit
function show_action_buttons(){
        const travelButton = document.getElementById('travel');
        travelButton.style.display = 'block';
        const searchButton = document.getElementById('search');
        searchButton.style.display = 'block';
        const bandage = document.getElementById('bandage');
        bandage.style.display = 'block';
}
//piilottaa tällä hetkellä kaikki nappulat
function hideButtons() {
    document.getElementById('loadgame').style.display = 'none';
    document.getElementById('newgame').style.display = 'none';
    document.getElementById('travel').style.display = 'none';
    document.getElementById('search').style.display = 'none';
    document.getElementById('bandage').style.display = 'none';
}
//LoadPlayer lähetys backendille
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

//NEW GAME "nappula" kuuntelija klikkaukseen
document.getElementById('newgame').addEventListener('click',newgame_button)
//NEW GAME Button
async function newgame_button () {
    playerName = prompt('Please enter your new player name:');
    if (playerName) {
        //jos saatu nimi lähetetään se addNewPlayerille ja odoetaan.
        await addNewPlayer(playerName);
        hideButtons();
        displayGameInfo();
        setTimeout(async () => {
            playerData = await loadPlayer(playerName);
            if (playerData && playerData.location) {
                // Keskitetään kartta pelaajan sijaintiin
                haeKaupunki(playerData.location);
                //näyttää action buttonit
                show_action_buttons();
                await fetchFarthestAirport(playerData.location);

            } else {
                console.log('Player not found.');
            }
            hideGameInfo();
        }, 5000); //  5 sekuntia
    }
}
//AddnewPlayer lähetysBackendille
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

function haeKaupunki(location, message = "You are here") {
    var url = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(location);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data && data.length > 0) {
                var lat = parseFloat(data[0].lat);
                var lon = parseFloat(data[0].lon);

                // Aseta näkymä ja zoomaustaso
                kartta.setView([lat, lon], 13); // Voit halutessasi poistaa tämän, jos et halua että kartan näkymä muuttuu

                // Näytä kartta-elementti ja päivitä sen koko
                var karttaElementti = document.getElementById('kartta');
                karttaElementti.style.display = 'block';
                kartta.invalidateSize();

                // Lisää merkki kartalle ja käytä annettua viestiä
                L.marker([lat, lon]).addTo(kartta)
                    .bindPopup(message).openPopup();


            } else {
                alert('Location not found for ' + location);
            }
        })
        .catch(error => {
            console.error('Error fetching location data for ' + location + ':', error);
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
async function fetchFarthestAirport(airportIdent) {
    try {
        const response = await fetch(`http://localhost:3000/playerdestination?ident=${encodeURIComponent(airportIdent)}`);
        const data = await response.json();
        if (data.farthest_airport_ident) {
            document.getElementById('destination').textContent = data.farthest_airport_ident;
            setTimeout(() => haeKaupunki(data.farthest_airport_ident, "You need to go here"), 2000);


        }
    } catch (error) {
        console.error('Error fetching farthest airport:', error);
        document.getElementById('destination').textContent = 'Error fetching data';
    }
}

async function display_player_stats(playerName)
{
    playerStats = await displayStats(playerName)
    const textContainer = document.getElementById("player_stats");
    let text = document.createTextNode(`LVL: ${playerStats.player_lvl}     EXP: ${playerStats.experience}/${playerStats.max_exp}     HP: ${playerStats.player_health}/${playerStats.max_hp}     BANDAGES: ${playerStats.bandage}     FUEL: ${playerStats.kerosene}`);
    textContainer.appendChild(text);
    // const StatsList = document.getElementById("player_stats");
    // let stats = "";
    // stats += `Level <li>${playerStats.player_lvl}</li>`;
    // stats += `experience <li>${playerStats.experience}</li>/${playerStats.max_exp}`;
    // stats += `HP <li>${playerStats.player_health}</li>/${playerStats.max_hp}`;
    // stats += `Bandages <li>${playerStats.bandage}</li>`;
    // stats += `Fuel <li>${playerStats.kerosene}</li>`;
    //
    // StatsList.innerHTML = stats;
    //lisää elementteihin haetut statsit
    show_player_stats()
}

async function displayStats(playerName) {
    try {
        const url = `http://localhost:3000/displayStats?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

function show_player_stats()
{
        const stats = document.getElementById('player_stats');
        stats.style.display = 'block';
}

function  hide_player_stats()
{
    document.getElementById('player_stats').style.display = 'none';
}