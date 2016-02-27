function drawDamageArc(ctx, bot){
	if(bot.rechargeTime > 0){
		var angle = Math.atan2(bot.heading.y, bot.heading.x);
		ctx.beginPath();
		ctx.moveTo(bot.pos.x, bot.pos.y);
		ctx.lineTo(bot.pos.x + 25*Math.cos(angle-Math.PI/4),
			   bot.pos.y + 25*Math.sin(angle-Math.PI/4));
		ctx.arc(bot.pos.x, bot.pos.y, 25, angle-Math.PI/4, angle+Math.PI/4);
		ctx.lineTo(bot.pos.x, bot.pos.y);
		ctx.closePath();
		ctx.fillStyle = "rgba(255,0,0," + bot.rechargeTime/10 + ")";
		ctx.fill();
		ctx.stroke();
	}
}

function drawHeadingLine(ctx, bot){
	// draw a line along the bot's heading
	var r = 10/Math.sqrt(Math.pow(bot.heading.x,2) + Math.pow(bot.heading.y,2));
	ctx.beginPath();
	ctx.moveTo(bot.pos.x, bot.pos.y);
	ctx.lineTo(bot.pos.x + r*bot.heading.x, bot.pos.y + r*bot.heading.y);
	ctx.stroke();
}

function drawBotBody(ctx, bot){
	ctx.beginPath();
	ctx.arc(bot.pos.x, bot.pos.y, 5, 0, 2*Math.PI);
	ctx.closePath();
	if(bot.health > 0){
		ctx.fillStyle = "white";
	} else {
		ctx.fillStyle = "grey";
	}
	ctx.fill();
	ctx.stroke();

	if(bot.health > 0){
		ctx.fillStyle = "black";
	} else {
		ctx.fillStyle = "grey";
	}
	ctx.font = "bold 12px Arial";
	ctx.fillText(bot.name, bot.pos.x, bot.pos.y+15);
}

function drawHealthBar(ctx, bot){
	if(bot.health > 0){
		ctx.beginPath();
		ctx.rect(bot.pos.x - 10, bot.pos.y - 15, 2*bot.health, 4);
		ctx.fillStyle = 'green';
		ctx.fill();
		ctx.stroke();
		ctx.beginPath();
		ctx.rect(bot.pos.x - 10 + 2*bot.health, bot.pos.y - 15, 2*(10-bot.health),4);
		ctx.fillStyle = 'red';
		ctx.fill();
		ctx.stroke();
	} else {
		ctx.beginPath();
		ctx.rect(bot.pos.x - 10, bot.pos.y - 15, 20, 4);
		ctx.fillStyle = 'grey';
		ctx.fill();
		ctx.stroke();
	}
}

// make sure that things are drawn in the correct order
function drawBots(ctx, bots){
	for(var i = 0; i < bots.length; i++) {
		drawDamageArc(ctx, bots[i]);
	}
	for(var i = 0; i < bots.length; i++) {
		drawHeadingLine(ctx, bots[i]);
	}
	for(var i = 0; i < bots.length; i++) {
		drawBotBody(ctx, bots[i]);
	}
	for(var i = 0; i < bots.length; i++) {
		drawHealthBar(ctx, bots[i]);
	}
}

function drawUpdate(event){
	var world = JSON.parse(event.data);
	var c = document.getElementById("mycanvas");
	var ctx = c.getContext("2d");
	ctx.clearRect(0, 0, c.width, c.height);
	alive_bots = world["bots"].filter(function(bot){ return bot.health > 0; });
	dead_bots = world["bots"].filter(function(bot){ return bot.health <= 0; });
	drawBots(ctx, dead_bots);
	drawBots(ctx, alive_bots);
}

