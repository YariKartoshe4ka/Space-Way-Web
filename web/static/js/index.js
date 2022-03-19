var rating = [
    [110, 'YariKartoshe4ka'],
    [93, 'Super Idol'],
    [80, 'GamerPro'],
    [79, 'NoobOrNoob'],
    [75, 'Better']
];

$(document).ready(function () {
    $.each(rating, function(i, [score, nick]) {
        let player = $(`
            <div class="nick place-${i + 1}">
                ${nick}
            </div>
            <div class="score place-${i + 1}">
                ${score}
            </div>
        `);

        $('#grid').append(player);
        player.hide();

        setTimeout(function () {
            player.animate({
                'opacity': 'show',
                'marginTop': '-3px',
                'fontSize': `115%`
            }, 1000);
        }, 1000 * i);
    });
});
