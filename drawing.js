function drawUpdate(event){
	var world = JSON.parse(event.data);
	var c = document.getElementById("mycanvas");
	var ctx = c.getContext("2d");
	ctx.clearRect(0, 0, c.width, c.height);
	for(var i = 0; i < world["bots"].length; i++) {
		var bot = world["bots"][i];
		ctx.beginPath();
		ctx.moveTo(bot.pos.x, bot.pos.y);
		ctx.lineTo(bot.pos.x + 25*bot.heading.x, bot.pos.y + 25*bot.heading.y);
		ctx.stroke();
		ctx.beginPath();
		ctx.arc(bot.pos.x, bot.pos.y, 5, 0, 2*Math.PI);
		ctx.stroke();
		ctx.fillStyle = "black";
		ctx.font = "bold 12px Arial";
		ctx.fillText(bot.name, bot.pos.x, bot.pos.y+15);
	}
}
