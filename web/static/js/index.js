var rating = [
    [110, 'YariKartoshe4ka'],
    [93, 'Super Idol'],
    [80, 'GamerPro'],
    [79, 'NoobOrNoob'],
    [75, 'Better']
];


$(document).ready(function () {
    $.each(rating, function(i, [score, nick]) {
        let player = $(`<p class="player">${score} ${nick}</p>`);
        $('#rating').append(player);
        player.hide();

        setTimeout(function () {
            player.fadeIn(1000);
        }, 1000 * i);

        console.log(i);
    });
});
