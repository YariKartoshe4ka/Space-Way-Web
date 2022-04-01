function choice(items, weights) {
    weights = weights.slice();
    let i;

    for (i = 0; i < weights.length; i++)
        weights[i] += weights[i - 1] || 0;

    let random = Math.random() * weights[weights.length - 1];

    for (i = 0; i < weights.length; i++)
        if (weights[i] > random)
            break;

    return items[i];
}


function generateBackground() {
    $('#background').hide().empty();

    let blockWidth = 100;
    let blockHeight = 80;
    let blockSpacing = 5;

    for (let i = 0; i < $(window).width(); i += blockWidth) {
        for (let j = 0; j < $(window).height(); j += blockHeight) {
            let image = choice(backgroundImages, backgroundImagesWeight);

            let x = Math.floor(Math.random() * (blockWidth - blockSpacing - image[1][0]) + i + blockSpacing);
            let y = Math.floor(Math.random() * (blockHeight - blockSpacing - image[1][1]) + j + blockSpacing);

            let img = $('<img>')
                .attr('src', image[0])
                .css({
                    'position': 'fixed',
                    'zIndex': -1,
                    'left': x + 'px',
                    'top': y + 'px',
                });

            $('#background').append(img);
        }
    }

    $('#background').show();
}


$(window).resize(generateBackground);
generateBackground();


$(document).ready(function() {
    $.getJSON('/api/get/', function(data) {
        $.each(data['result'], function(i, [score, nick]) {
            ++i;

            let player = $(`
                <div class="nick">
                    ${nick}
                </div>
                <div class="score place-${i}">
                    ${score}
                </div>
            `);

            player.hide();
            $('#grid').append(player);

            setTimeout(function() {
                player.animate({
                    'opacity': 'show',
                    'marginTop': '-3px',
                    'fontSize': `${Math.round(parseInt(player.css('fontSize')) * 1.15)}px`
                }, 1000);
            }, 1000 * (i - 1));
        });
    });
});
