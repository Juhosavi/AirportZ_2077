let screen_name = null;
let new_location = null;
let enemyAmount = 0;
let new_icao = null; //'new_airport' <-- icaoon viitataan tolla
let enemy_stats = null; //'enemy_lvl', 'enemy_hp', 'min_dmg', 'max_dmg', 'exp'
let player_stats = null;//'player_lvl', 'experience', 'player_health', 'bandage', 'kerosene', 'max_exp', 'max_hp'

function hide_enemies()
{
    //hide enemies
    document.getElementById('enemy1').style.display = 'none';
    document.getElementById('first_HP_bg').style.display = 'none';
    document.getElementById('first_HP_red').style.display = 'none';

    document.getElementById('enemy2').style.display = 'none';
    document.getElementById('second_HP_bg').style.display = 'none';
    document.getElementById('second_HP_red').style.display = 'none';

    document.getElementById('enemy3').style.display = 'none';
    document.getElementById('third_HP_bg').style.display = 'none';
    document.getElementById('third_HP_red').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', async function()
{
    hide_enemies();
    enemyAmount = Math.floor(Math.random() * 4) + 1;
    let urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('parameter1') && urlParams.has('parameter2'))
    {
        screen_name = urlParams.get('parameter1');
        new_location = urlParams.get('parameter2');
        await get_new_icao();
        await get_enemyStats();
        await get_playerStats();
        await display_player_stats();
        await display_enemies();

        console.log('Parameter value:', screen_name, new_location);
        console.log(enemyAmount);

    }
    else
    {
        console.log('Parameter not found');
    }
});

async function get_new_icao()
{
    new_icao = await getICAO();
    console.log(new_icao.new_airport);
}

async function getICAO()
{
    try {
        const url = `http://localhost:3000/getSelectedAirportICAO?name=${encodeURIComponent(new_location)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function get_enemyStats()
{
    enemy_stats = await getEnemy();
    console.log(enemy_stats.enemy_lvl);
}

async function getEnemy()
{
    try {
        const url = `http://localhost:3000/getEnemyStats?name=${encodeURIComponent(new_icao.new_airport)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function get_playerStats()
{
    player_stats = await getPlayer();
    console.log(player_stats.player_health);
}

async function getPlayer()
{
    try {
        const url = `http://localhost:3000/displayStats?name=${encodeURIComponent(screen_name)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function display_player_stats()
{
    const textContainer = document.getElementById("player_stats");
    textContainer.innerHTML = "";
    let text = document.createTextNode(`LVL: ${player_stats.player_lvl}   HP: ${player_stats.player_health}/${player_stats.max_hp}   BANDAGES: ${player_stats.bandage}`);
    textContainer.appendChild(text);
}

async function display_enemies()
{
    if (enemyAmount === 1)
    {
        document.getElementById('enemy1').style.display = 'block';
        document.getElementById('first_HP_bg').style.display = 'block';
        document.getElementById('first_HP_red').style.display = 'block';
    }
    else if (enemyAmount === 2)
    {
        document.getElementById('enemy1').style.display = 'block';
        document.getElementById('first_HP_bg').style.display = 'block';
        document.getElementById('first_HP_red').style.display = 'block';

        document.getElementById('enemy2').style.display = 'block';
        document.getElementById('second_HP_bg').style.display = 'block';
        document.getElementById('second_HP_red').style.display = 'block';
    }
    else
    {
        document.getElementById('enemy1').style.display = 'block';
        document.getElementById('first_HP_bg').style.display = 'block';
        document.getElementById('first_HP_red').style.display = 'block';

        document.getElementById('enemy2').style.display = 'block';
        document.getElementById('second_HP_bg').style.display = 'block';
        document.getElementById('second_HP_red').style.display = 'block';

        document.getElementById('enemy3').style.display = 'block';
        document.getElementById('third_HP_bg').style.display = 'block';
        document.getElementById('third_HP_red').style.display = 'block';
    }
}