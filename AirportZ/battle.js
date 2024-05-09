'use strict'

let screen_name = null;
let new_location = null;
let enemyAmount = 0;
let new_icao = null; //'new_airport' <-- icaoon viitataan tolla
let enemy_stats = null; //'enemy_lvl', 'enemy_hp', 'min_dmg', 'max_dmg', 'exper'
let player_stats = null;//'player_lvl', 'experience', 'player_health', 'bandage', 'kerosene', 'max_exp', 'max_hp', 'destination', 'battles_won'
let enemy_list = [];
let player_dmg = null;//min_dmg, max_dmg
const first_red = document.getElementById("first_HP_red");
const second_red = document.getElementById("second_HP_red");
const third_red = document.getElementById("third_HP_red");
let width1 = 11.5;
let width2 = 11.5;
let width3 = 11.5;
let player_takes_dmg = null;
let exp_earned = null;

document.getElementById("blinkingText2").style.display = 'none';
document.getElementById("blinkingText").style.display = 'none';
document.getElementById("death").style.display = 'none';

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
    enemyAmount = Math.floor(Math.random() * 3) + 1;
    let urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('parameter1') && urlParams.has('parameter2'))
    {
        screen_name = urlParams.get('parameter1');
        new_location = urlParams.get('parameter2');
        await get_new_icao();
        await get_enemyStats();
        await get_playerStats();
        await display_player_stats();
        await get_player_dmg();
        await display_enemies();
        enemy_list = await get_objects();
        await add_enemy_listeners();
        // console.log(enemy_list[0].hp)
        //
        // console.log('Parameter value:', screen_name, new_location);
        // console.log(enemyAmount);

    }
    else
    {
        console.log('Parameter not found');
    }
});

async function get_new_icao()
{
    new_icao = await getICAO();
    // console.log(new_icao.new_airport);
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
    // console.log(enemy_stats.enemy_lvl);
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

async function get_player_dmg()
{
    player_dmg = await getPlayerDmg();
}
async function getPlayerDmg()
{
    try {
        const url = `http://localhost:3000/getPlayerDmg?name=${encodeURIComponent(player_stats.player_lvl)}`;
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
    let text = document.createTextNode(`LVL: ${player_stats.player_lvl}   HP: ${player_stats.player_health}/${player_stats.max_hp}   BANDAGES: ${player_stats.bandage}                  ENEMY LVL: ${enemy_stats.enemy_lvl}`);
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

async function get_objects()
{
    const enemyList = [];

    for (let i = 0; i < enemyAmount; i++)
    {
        let zombie = new Enemy(i+1, enemy_stats.enemy_lvl, enemy_stats.enemy_hp, enemy_stats.min_dmg, enemy_stats.max_dmg, enemy_stats.exp);
        enemyList.push(zombie);
    }
    return enemyList;
}

class Enemy
{
    constructor(number, lvl, hp, min_dmg, max_dmg, exp)
    {
        this.lvl = lvl;
        this.hp = hp;
        this.min_dmg = min_dmg;
        this.max_dmg = max_dmg;
        this.exp = exp;
        this.number = number;

    }
    take_dmg(dmg)
    {
        this.hp = this.hp - dmg;
    }
}

async function add_enemy_listeners()
{
    await playerTurnText();
    console.log("adding listeners")
    document.querySelectorAll('.clickPlayer').forEach(function (img) {
        img.addEventListener('click', playerHeal);
    });
    document.querySelectorAll('.clickable1').forEach(function (img) {
        img.addEventListener('click', handleClick1);
    });

    document.querySelectorAll('.clickable2').forEach(function (img) {
        img.addEventListener('click', handleClick2);
    });

    document.querySelectorAll('.clickable3').forEach(function (img) {
        img.addEventListener('click', handleClick3);
    });
}

async function remove_enemy_listeners(){

    await enemyTurnText();
    document.querySelectorAll('.clickPlayer').forEach(function (img) {
        img.removeEventListener('click', playerHeal);
    });
    document.querySelectorAll('.clickable1').forEach(function (img) {
        img.removeEventListener('click', handleClick1);
    });
    document.querySelectorAll('.clickable2').forEach(function (img) {
        img.removeEventListener('click', handleClick2);
    });
    document.querySelectorAll('.clickable3').forEach(function (img) {
        img.removeEventListener('click', handleClick3);
    });
    await player_take_dmg();

}


async function playerHeal(event)
{
    if (event.target.classList.contains('clickPlayer'))
    {
        if (player_stats.bandage > 0)
            if (player_stats.player_health < player_stats.max_hp)
                if (player_stats.player_health > 50 && player_stats.max_hp === 100)
                {
                    player_stats.player_health = 100;
                    player_stats.bandage = player_stats.bandage - 1;
                    alert(`You used a bandage! Your health is now ${player_stats.player_health}`)
                }
                else if (player_stats.player_health > 100 && player_stats.max_hp === 150)
                {
                    player_stats.player_health = 150;
                    player_stats.bandage = player_stats.bandage - 1;
                    alert(`You used a bandage! Your health is now ${player_stats.player_health}`)
                }
                else if (player_stats.player_health > 150 && player_stats.max_hp === 200)
                {
                    player_stats.player_health = 200;
                    player_stats.bandage = player_stats.bandage - 1;
                    alert(`You used a bandage! Your health is now ${player_stats.player_health}`)
                }
                else
                {
                    player_stats.player_health = player_stats.player_health + 50;
                    player_stats.bandage = player_stats.bandage - 1;
                    alert(`You used a bandage! Your health is now ${player_stats.player_health}`)
                }
            else
            {
                alert("Your health is already full.")
            }
        else
        {
            alert("You have no bandages!");
        }
    }
    await display_player_stats();
    await remove_enemy_listeners();
}

async function handleClick1(event) {
    // Check if the clicked image has the "special-image" class
    if (event.target.classList.contains('clickable1')) {
        // Add your custom click behavior here
        console.log('Special image 1 clicked!');
        let damage = Math.floor(Math.random() * (player_dmg.max_dmg - player_dmg.min_dmg + 1)) + player_dmg.min_dmg;
        console.log(`dmg ${damage}`);
        console.log(`hp ${enemy_list[0].hp}`);
        width1 = width1 - (width1 * (damage / enemy_list[0].hp));
        enemy_list[0].take_dmg(damage);
        if (width1 <= 0) {
            enemyAmount = enemyAmount - 1;
            first_red.style.display = 'none';
            document.getElementById('enemy1').style.display = 'none';
            document.getElementById('first_HP_bg').style.display = 'none';
            exp_earned = exp_earned + enemy_stats.exper;
            if (enemyAmount === 0)
            {
                await victory();
            }
        }
        else {
            first_red.style.width = `${width1}%`;
        }
        console.log(`new hp ${enemy_list[0].hp}`);

    } else {
        // Handle click for other images (if needed)
        console.log('Regular image clicked!');
    }
    if (enemyAmount !== 0)
    {
        await remove_enemy_listeners();
    }
    else
    {
        document.getElementById("blinkingText").style.display = 'none';
    }
}

async function handleClick2(event) {
    if (event.target.classList.contains('clickable2')) {
        console.log('Special image 2 clicked!');
        let damage = Math.floor(Math.random() * (player_dmg.max_dmg - player_dmg.min_dmg + 1)) + player_dmg.min_dmg;
        console.log(`dmg ${damage}`);
        console.log(`hp ${enemy_list[1].hp}`);
        width2 = width2 - (width2 * (damage / enemy_list[1].hp));
        enemy_list[1].take_dmg(damage);
        if (width2 <= 0) {
            enemyAmount = enemyAmount - 1;
            second_red.style.display = 'none';
            document.getElementById('enemy2').style.display = 'none';
            document.getElementById('second_HP_bg').style.display = 'none';
            exp_earned = exp_earned + enemy_stats.exper;
            if (enemyAmount === 0)
            {
                await victory();
            }
        }
        else {
            second_red.style.width = `${width2}%`;
        }
        console.log(`new hp ${enemy_list[1].hp}`)

    } else {
        // Handle click for other images (if needed)
        console.log('Regular image clicked!');
    }
    if (enemyAmount !== 0)
    {
        await remove_enemy_listeners();
    }
    else
    {
        document.getElementById("blinkingText").style.display = 'none';
    }
}

async function handleClick3(event) {
    // Check if the clicked image has the "special-image" class
    if (event.target.classList.contains('clickable3')) {
        console.log('Special image 3 clicked!');
        let damage = Math.floor(Math.random() * (player_dmg.max_dmg - player_dmg.min_dmg + 1)) + player_dmg.min_dmg;
        console.log(`dmg ${damage}`);
        console.log(`hp ${enemy_list[2].hp}`);
        width3 = width3 - (width3 * (damage / enemy_list[2].hp));
        enemy_list[2].take_dmg(damage);
        if (width3 <= 0) {
            enemyAmount = enemyAmount - 1;
            third_red.style.display = 'none';
            document.getElementById('enemy3').style.display = 'none';
            document.getElementById('third_HP_bg').style.display = 'none';
            exp_earned = exp_earned + enemy_stats.exper;
            if (enemyAmount === 0)
            {
                await victory();
            }
        }
        else {
            third_red.style.width = `${width3}%`;
        }
        console.log(`new hp ${enemy_list[2].hp}`);

    } else {
        // Handle click for other images (if needed)
        console.log('Regular image clicked!');
    }
    if (enemyAmount !== 0)
    {
        await remove_enemy_listeners();
    }
    else
    {
        document.getElementById("blinkingText").style.display = 'none';
    }
}


async function player_take_dmg()
{
    let duration = 2000;
    for (let i = 0; i < enemyAmount; i++)
    {
        setTimeout(function()
        {
            player_takes_dmg = Math.floor(Math.random() * (enemy_stats.max_dmg - enemy_stats.min_dmg + 1)) + enemy_stats.min_dmg;
            alert(`Zombie ${i+1} hits you for ${player_takes_dmg} points!`)
            player_stats.player_health = player_stats.player_health - player_takes_dmg;
            if (player_stats.player_health <= 0)
            {
                player_dies();
            }
            display_player_stats();
            add_enemy_listeners();
        }, duration);
    }
    // await add_enemy_listeners();
}

async function playerTurnText() {
    console.log("kutsuttiin playerturntext")
    document.getElementById("blinkingText").style.display = 'block';
    document.getElementById("blinkingText2").style.display = 'none';
}

async function enemyTurnText()
{
    console.log("kutsuttiin enemyturntext")
    document.getElementById("blinkingText2").style.display = 'block';
    document.getElementById("blinkingText").style.display = 'none';
}

function player_dies()
{
    hide_enemies();
    document.getElementById("death").style.display = 'block';
    let duration = 4000;
    setTimeout(function()
        {
            window.location.href = 'main.html';
        }, duration);
}

async function victory()
{
    console.log("you win!")
    document.getElementById("blinkingText2").style.display = 'none';
    player_stats.experience = player_stats.experience + exp_earned;

    win_battle_text();
    if (player_stats.max_exp === 10 && player_stats.experience >= 10)
    {
        player_stats.player_lvl = 2;
        alert(`You leveled up! Your level is now ${player_stats.player_lvl}`)
    }
    else if (player_stats.max_exp === 20 && player_stats.experience >= 20)
    {
        player_stats.player_lvl = 3;
        alert(`You leveled up! Your level is now ${player_stats.player_lvl}`)
    }

    await battle_victory()
    let duration = 3000;
    setTimeout(function()
    {
        if (new_icao.new_airport === player_stats.destination)
        {
            window.location.href = 'destination.html?parameter1=' + encodeURIComponent(screen_name) + '&parameter2=' + encodeURIComponent(player_stats.battles_won);
        }
        else {
            window.location.href = 'travel.html?parameter1=' + encodeURIComponent(screen_name);
        }
    }, duration);
}

async function battle_victory()
{
    let test = await battleVictory();
    console.log(`${test.affirm}`);
}
async function battleVictory()
{
    try {
        const url = `http://localhost:3000/battleVictory?name=${encodeURIComponent(screen_name)}&new_location=${encodeURIComponent(new_icao.new_airport)}&experience=${encodeURIComponent(player_stats.experience)}&player_hp=${encodeURIComponent(player_stats.player_health)}&bandage=${encodeURIComponent(player_stats.bandage)}&player_lvl=${encodeURIComponent(player_stats.player_lvl)}`;
        const response = await fetch(url);
        const jsonPlayer = await response.json();

        return jsonPlayer;
    } catch (error) {
        console.log(error.message);
    }
}

async function win_battle_text()
{
    let text = `You won the battle!`;
    text = text.replace(/\n/g, "<br>");
    document.getElementById('battle_win').innerHTML = text;

}
