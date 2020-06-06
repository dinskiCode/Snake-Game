var light_green = "#83eb34";
var green = "#30db33";

function start_game() {
    game_area.start();
    head = new body_part(true, [100, 100]);
    apple = new apple();
}

var game_area = {
    canvas : document.createElement("canvas"),
    start : function() {
        this.canvas.width = 650;
        this.canvas.height = 650;
        this.ctx = this.canvas.getContext("2d");
        draw_background(this.ctx);
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
        this.interval = setInterval(update_game_area, 150);
        window.addEventListener('keydown', function(e) {
            game_area.key = e.keyCode;
        })
    },
    clear : function() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        draw_background(this.ctx);
    },
    game_started : false,
    game_over : false,
    score : 0,
}

function draw_background(context) {
    for (var i = 0; i < game_area.canvas.width/50; i++) {
        for (var k = 0; k < game_area.canvas.height/50; k++) {
            if (i%2 == 0) {
                if (k%2 == 0) {
                    context.fillStyle = light_green;
                    context.fillRect(i*50, k*50, 50, 50);
                } else {
                    context.fillStyle = green;
                    context.fillRect(i*50, k*50, 50, 50);
                }
            } else {
                if (k%2 == 0) {
                    context.fillStyle = green;
                    context.fillRect(i*50, k*50, 50, 50);
                } else {
                    context.fillStyle = light_green;
                    context.fillRect(i*50, k*50, 50, 50);
                }
            }
        }
    }
}

function body_part(is_head, pos) {
    speed = 50;
    this.width = this.height = 50;
    this.is_head = is_head
    if (this.is_head == true) {
        this.color = "black";
    } else {
        this.color = "blue";
    }
    this.x = pos[0];
    this.y = pos[1];
    this.move_dir = "";
    this.png = null;
    ctx = game_area.ctx;
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.width, this.height);
    body.body_array.push(this);

    this.update = function() {
        ctx = game_area.ctx;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x + 5, this.y + 5, this.width - 10, this.height - 10);
    }

    this.check_apple_eaten = function(apple_object) {
        ate_apple = false;
        if (this.x == apple_object.x && this.y == apple_object.y) {
            ate_apple = true;
            game_area.score += 1;
        }
        return ate_apple;
    }

    this.check_self_collision = function() {
        if (body.body_array.length > 1) {
            for (var i = 1; i < body.body_array.length - 1; i++) {
                if (body.body_array[0].x == body.body_array[i].x && body.body_array[0].y == body.body_array[i].y) {
                    alert("You lose. Your score: " + game_area.score);
                    game_area.game_over = true;
                }
            }
        }
    }

    this.check_border_collision = function() {
        if (body.body_array[0].x > game_area.canvas.width - 1 || body.body_array[0].x < 0 ||
        body.body_array[0].y > game_area.height - 1 || body.body_array[0].y < 0) {
            game_area.game_over = true;
            alert("You lose. Your score: " + game_area.score);
        }
    }
}


function apple() {
    this.color = "red";
    this.width = this.height = 40;
    this.x = Math.floor(Math.random() * 13) * 50;
    this.y = Math.floor(Math.random() * 10) * 50;
    ctx = game_area.ctx;
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.width, this.height);

    this.update = function() {
        ctx = game_area.ctx;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x + 5, this.y + 5, this.width, this.height);
    }

    this.random_move = function() {
        var new_x = Math.floor(Math.random() * 13) * 50;
        var new_y = Math.floor(Math.random() * 10) * 50;
        this.x = new_x;
        this.y = new_y;
    }
}

// only if game_started = true ?
function update_game_area() {   // if move_dir == ..., move_all_body_parts etc. in here?
    if (game_area.game_over == false) {
        game_area.clear();

        if (game_area.key) {
            game_area.game_started = true;
        }

        if (body.head_pos.length > body.body_array.length) {
            body.head_pos.shift();
        }

        if (game_area.key && game_area.key == 37) {
            body.body_array[0].x -= 50;
            body.body_array[0].move_dir = "left";
        }
        if (game_area.key && game_area.key == 39) {
            body.body_array[0].x += 50;
            body.body_array[0].move_dir = "right";
        }
        if (game_area.key && game_area.key == 38) {
            body.body_array[0].y -= 50;
            body.body_array[0].move_dir = "up";
        }
        if (game_area.key && game_area.key == 40) {
            body.body_array[0].y += 50;
            body.body_array[0].move_dir = "down";
        }

        if (game_area.game_started == true) {
            body.head_pos.push([body.body_array[0].x, body.body_array[0].y]);
        }

        // create new body part if apple is eaten
        if (body.body_array[0].check_apple_eaten(apple)) {
            body_part_obj = new body_part(false, [body.head_pos[body.head_pos.length - 1 - body.body_array.length][0], body.head_pos[body.head_pos.length - 1 - body.body_array.length][1]]);
            body_part_obj.move_dir = body.body_array[body.body_array.length - 2].move_dir;
            apple.random_move();
        }

        // move every body part one position forward
        var body_nr = 1;
        for (var i = body.body_array.length - 1; i > 0; i--) {
            body.body_array[i].x = body.head_pos[body.head_pos.length - 1 - body_nr][0];
            body.body_array[i].y = body.head_pos[body.head_pos.length - 1 - body_nr][1];
            body.body_array[i].move_dir = body.body_array[body.body_array.length - 1 - body_nr].move_dir;
            body_nr += 1;
        }

        // update the snake body
        for (var i = 0; i < body.body_array.length; i++) {
            body.body_array[i].update();
        }
        body.body_array[0].check_self_collision();
        body.body_array[0].check_border_collision();
        apple.update();
    }
    if (game_area.game_over == true) {
        start_game();
        game_area.game_over = false;
    }
}

var body = {
    body_array : [],
    head_pos : [],
    move_dir : ""
}
