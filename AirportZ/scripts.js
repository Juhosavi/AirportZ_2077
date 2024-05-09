'use strict';
let playerName;
let playerData = null;


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
            window.location.href = 'travel.html?parameter1=' + encodeURIComponent(playerName);
        } else {
            console.log('Player not found.');
        }
    }
}

//piilottaa tällä hetkellä kaikki nappulat
function hideButtons() {
    document.getElementById('loadgame').style.display = 'none';
    document.getElementById('newgame').style.display = 'none';
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
                console.log("added new player.")
            } else {
                console.log('Player not found.');
            }
            hideGameInfo();
            window.location.href = 'travel.html?parameter1=' + encodeURIComponent(playerName);
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
