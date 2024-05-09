'use strict';
let playerName;
let playerData = null;
let playerStats = null;
let closestAirports = null;
let gifUrl = 'https://media1.tenor.com/m/NnBsjb10pUYAAAAd/airbus-airplane.gif';
let foundItems = null;
let location_coords = null;//viittaa latitudeen location_coords.latitude <--long - samalla tavalla mut .longitude
let destination_coords = null;//viittaa kuten yllä
let destinationICAO = null;
let searchedAirport = false;
let airport_levels = null;
let new_location = null;


document.getElementById('travel').style.display = 'block';
document.getElementById('search').style.display = 'block';
document.getElementById('bandage').style.display = 'block';
document.getElementById('destination').style.display = 'block';


document.addEventListener('DOMContentLoaded', async function()
{
    let urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('parameter1'))
    {
        playerName = urlParams.get('parameter1');
        await load_game_button();
    }
    else
    {
        console.log('Parameter not found');
    }
});


document.getElementById('travel').addEventListener('click', get_closest_airports)

//LOAD GAME BUTTON
async function load_game_button() {
    if (playerName) {
        // Haetaan pelaajan tiedot load player funktiosta ja odotetaan awaitilla
        playerData = await loadPlayer(playerName);
        // Tarkistetaan, onko pelaajan tiedot saatu
        if (playerData && playerData.location) {
            await getLocationCoords()
            // Keskitetään kartta pelaajan sijaintiin
            haeKaupunki(location_coords.latitude, location_coords.longitude);
            //näyttää action buttonit
            show_action_buttons();
            await display_player_stats(playerName)
            await fetchFarthestAirport(playerData.location);
            document.getElementById('destination').style.display = 'block';
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

function hide_action_buttons()
{
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


let kartta = L.map('kartta');
let karttaTaso = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(kartta);

function haeKaupunki(latitude, longitude, message = "You are here") {
    // Aseta näkymä ja zoomaustaso
    kartta.setView([latitude, longitude], 13); // Voit halutessasi poistaa tämän, jos et halua että kartan näkymä muuttuu

    // Näytä kartta-elementti ja päivitä sen koko
    let karttaElementti = document.getElementById('kartta');
    karttaElementti.style.display = 'block';
    kartta.invalidateSize();

    // Lisää merkki kartalle ja käytä annettua viestiä
    L.marker([latitude, longitude]).addTo(kartta)
        .bindPopup(message).openPopup();
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
        document.getElementById('destination').textContent = 'Destination: ' + destinationICAO.destination_name;
        setTimeout(() => haeKaupunki(destination_coords.latitude, destination_coords.longitude, "You need to travel here"), 2000);
    } catch (error) {
        console.error('Error fetching farthest airport:', error);
        document.getElementById('destination').textContent = 'Error fetching data';
    }
}

document.getElementById('search').addEventListener('click', search_button);

async function search_button()
{
    if (searchedAirport === false)
    {
        console.log(playerName);
        foundItems = await searchAirport(playerName);
        alert(`You found ${foundItems.bandage} bandage(s) and ${foundItems.fuel} fuel!`);
        await display_player_stats();
        searchedAirport = true;
    }
    else
        alert("You have already searched this airport.")
}

async function searchAirport(playerName)
{
    try {
        const url = `http://localhost:3000/searchAirport?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

document.getElementById('bandage').addEventListener('click', use_bandage);

async function use_bandage()
{
    if (playerStats.bandage <= 0)
    {
        alert("You have no bandages!")
    }
    else
    {
        if (playerStats.player_health === playerStats.max_hp)
        {
            alert("Your health is already full.")
        }
        else
        {
            await use_a_bandage()
            await update_health()
            await display_player_stats()
        }
    }

}
async function update_health()
{
    try {
        const url = `http://localhost:3000/updateHealth?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function use_a_bandage()
{
    try {
        const url = `http://localhost:3000/useBandage?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function getLocationCoords()
{
    console.log(playerData.location);
    location_coords = await getLocationCoordinates();
    await getDestinationCoordinates();
    console.log(location_coords.latitude);
    console.log(destination_coords.latitude);
}

async function getLocationCoordinates() {
    try {
        const url = `http://localhost:3000/getCoordinates?name=${encodeURIComponent(playerData.location)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function getDestinationCoordinates()
{
    destinationICAO = await getDestinationICAO();
    console.log(destinationICAO.destination);
    destination_coords = await getDestinationCoords();
}

async function getDestinationCoords() {
    try {
        const url = `http://localhost:3000/getCoordinates?name=${encodeURIComponent(destinationICAO.destination)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}
async function getDestinationICAO()
{
    try {
        const url = `http://localhost:3000/getDestination?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function display_player_stats()
{
    playerStats = await displayStats();
    const textContainer = document.getElementById("player_stats");
    textContainer.innerHTML = "";
    let text = document.createTextNode(`LVL: ${playerStats.player_lvl}     EXP: ${playerStats.experience}/${playerStats.max_exp}     HP: ${playerStats.player_health}/${playerStats.max_hp}     BANDAGES: ${playerStats.bandage}     FUEL: ${playerStats.kerosene}`);
    textContainer.appendChild(text);
    show_player_stats()
}

async function displayStats() {
    try {
        const url = `http://localhost:3000/displayStats?name=${encodeURIComponent(playerName)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function get_closest_airports(location)
{
    hide_action_buttons();
    show_travel_dropdown();
    closestAirports = await getAirports(location);
    await get_airport_levels();
    console.log(closestAirports.airport1);
    document.addEventListener("DOMContentLoaded", fill_airport_dropdown);
    fill_airport_dropdown(closestAirports);
}

async function get_airport_levels()
{
    airport_levels = await getLevels();
}

async function getLevels()
{
    try {
        const url = `http://localhost:3000/getAirportLevels?airport1=${encodeURIComponent(closestAirports.airport1)}&airport2=${encodeURIComponent(closestAirports.airport2)}&airport3=${encodeURIComponent(closestAirports.airport3)}&airport4=${encodeURIComponent(closestAirports.airport4)}&airport5=${encodeURIComponent(closestAirports.airport5)}&airport6=${encodeURIComponent(closestAirports.airport6)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

function fill_airport_dropdown(closestAirports) {
    const selectElement = document.getElementById("airportSelect");
    selectElement.innerHTML = '';

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select an airport";
    selectElement.appendChild(defaultOption);

    const airports = [closestAirports.airport1, closestAirports.airport2, closestAirports.airport3, closestAirports.airport4, closestAirports.airport5, closestAirports.airport6];
    const levels = [airport_levels.level1, airport_levels.level2, airport_levels.level3, airport_levels.level4, airport_levels.level5, airport_levels.level6];

    airports.forEach((airport, index) => {
        const option = document.createElement("option");
        option.value = airport;
        option.textContent = airport + " - Lvl. " + levels[index];
        selectElement.appendChild(option);
    });
}

let selectedAirport = 'null';

document.getElementById("travel_confirm").addEventListener("click", handleTravelConfirm);
function handleTravelConfirm() {
    selectedAirport = document.getElementById("airportSelect").value;

        if (selectedAirport)
        {
            alert(`You selected: ${selectedAirport}`);
        // siirtyminen uuteen locaan?
            document.getElementById('kartta').style.display = 'none';
            hide_action_buttons();
            hide_travel_dropdown()
            loadGif(gifUrl);
        }
        else
        {
            alert("Please select an airport before confirming.");
        }
}

function loadGif(url)
{
    document.getElementById('destination').style.display = 'none';
    let gifContainer = document.getElementById('gifContainer');
    let img = document.createElement('img');
    img.src = url;
    gifContainer.appendChild(img);
    let duration = 10000;
    setTimeout(function() {
        gifContainer.removeChild(img);
        // loadBattleBG(battle_bg)
        //loadaa battle-sivu! Lähetä tieto uudesta kentästä (ICAO) sekä pelaajan nimi
        window.location.href = 'battle.html?parameter1=' + encodeURIComponent(playerName) + '&parameter2=' + encodeURIComponent(selectedAirport);
    }, duration);
}


async function getAirports(location) {
    try {
        const url = `http://localhost:3000/getCloseAirports?name=${encodeURIComponent(playerData.location)}`;
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

function show_travel_dropdown()
{
    const travel_dropdown = document.getElementById('airportSelect');
    travel_dropdown.style.display = 'block';
    const travel_confirm = document.getElementById('travel_confirm');
    travel_confirm.style.display = 'block';
}

function hide_travel_dropdown()
{
    document.getElementById('airportSelect').style.display = 'none';
    document.getElementById('travel_confirm').style.display = 'none';
}
