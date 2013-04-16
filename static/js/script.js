$(function() {
    $('#myModal').modal('toggle');
    $('button#start').click(function(){
        game_name = $("form#new_game #game_name").val();
        players_max = $("form#new_game #players_max").val();
        if (game_name == '')
            game_name = "Let's Play!"
        game_stringified = JSON.stringify( {
                name: game_name,
                id: Math.floor(Math.random()*100000),
                players_max: players_max,
                players_current: "0"
            });
        $.post("/games", { 'newgame':game_stringified})
        .done(function(data) {
            if (data['result']=='ok')
                window.location.href = "/game/"+data['id'];
        });
    });


    $('#bet button').click(function(){
        tokens = $("#bet input[name='tokens']").val();
        player_id = $("#bet input[name='player_id']").val();
        game_id = $("#bet input[name='game_id']").val();
        console.log(player_id)
        action= {
                player_id: player_id,
                action: "bet",
                value: tokens,
            };
        $.post("/game/"+game_id+"/action", action)
        .done(function(data) {
            if (data=='ok')
                window.location.reload();
            else
                console.log(data)
        });
    });


    // compile the template
    compiled = dust.compile($("#game-list-template").html(),"tpl");

    // load the compiled template into the dust template cache
    dust.loadSource(compiled);

    var template = function(games) {	
        var result;	
        dust.render("tpl", games, function(err, res) {
            result = res;
        });	
        return result;
    };

    $.get("/games")
    .done(function(data) {
        template_json = {"games":data};
        $("#games").html(template(template_json));
        $('.pretty-date').text(function(index, text) {
            if(text!="")
                return moment(text).fromNow();
        });
    });
});
