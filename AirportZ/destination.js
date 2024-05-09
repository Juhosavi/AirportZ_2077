'use strict'
let screen_name = null;
let battles_won = null;


document.addEventListener('DOMContentLoaded', async function() {
    let urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('parameter1') && urlParams.has('parameter2')) {
        screen_name = urlParams.get('parameter1');
        battles_won = urlParams.get('parameter2');
        console.log(`battles won: ${battles_won}`)
        await get_battles();
    }
     else
    {
        console.log('Parameter not found');
    }
});

async function get_battles()
{
    let text = `\n\n\n\nCongratulations!\n\nYou made it to your destination!\n\nYou won ${battles_won} battles during your journey.\n\n\n\n\n\n`;
    text = text.replace(/\n/g, "<br>");
    document.getElementById('end_game_info').innerHTML = text;

}