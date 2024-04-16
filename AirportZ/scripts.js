'use strict';

document.getElementById('loadgame').addEventListener('click', async function() {
    const playerName = prompt('Please enter your player name:');
    if (playerName) {
        await loadPlayer(playerName);
    } else {
        console.log('Player name not entered.');
    }
});


async function loadPlayer(playerName) {
    try {
        const url = `http://localhost:3000/loadPlayer?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        if (jsonPlayer.error) {
            console.log('Player not found.');
        } else {
            console.log('Player data:', jsonPlayer);
        }
    } catch (error) {
        console.log(error.message);
    } finally {
        console.log('Load player attempt complete');
    }
}

document.getElementById('newgame').addEventListener('click', async function() {
    const playerName = prompt('Please enter your new player name:');
    if (playerName) {
        await addNewPlayer(playerName);
    } else {
        console.log('Player name not entered.');
    }
});
async function addNewPlayer(playerName) {
    try {
        const url = `http://localhost:3000/addPlayer`;
        const playerData = { name: playerName };

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Add this line to send the playerData in the request body
            body: JSON.stringify(playerData)
        });

        const jsonResponse = await response.json();
        // ... rest of your code
    } catch (error) {
        console.log(error.message);
    } finally {
        console.log('New player attempt complete');
    }
}

