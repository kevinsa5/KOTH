timecount = 0;
timedelay = 100;
var incrementTimeCount = function() {
  var pbar = document.getElementById('pbar');
  pbar.value = timecount;
  pbar.getElementsByTagName('span')[0].innerHTML = timecount;
  timecount += timedelay;
  if(timecount > 1000){
    document.getElementById('loading').style.visibility="visible";
  }
}

window.setInterval(incrementTimeCount, timedelay);

function initSSE(){
  var source = new EventSource("/cgi-bin/redis-relay.cgi");
  source.onopen = function(event){
    //setTimeout(function(){
    //  document.getElementById('loading').style.visibility="hidden";
    //}, 1000);
  }
  source.onmessage = function(event){
    // from drawing.js:
    drawUpdate(event);
    var world = JSON.parse(event.data);    
    timecount = 0;
    document.getElementById('loading').style.visibility="hidden";
    // update the table of bot variables
    var table = document.createElement('table');
    var attr = document.createAttribute('border');
    attr.value = "1";
    table.setAttributeNode(attr);
    var tr = document.createElement('tr');
    var cols = ["name","position","heading","health","note"]
    for(var i = 0; i < cols.length; i++){
      var th = document.createElement('th');
      th.appendChild(document.createTextNode(cols[i]));
      tr.appendChild(th);
    }
    table.appendChild(tr);
    for(var i = 0; i < world["bots"].length; i++) {
      var bot = world["bots"][i];
      var tr = document.createElement('tr');
      var name = document.createElement('td');
      var pos = document.createElement('td');
      var heading = document.createElement('td');
      var health = document.createElement('td');
      var note = document.createElement('td');
      name.appendChild(document.createTextNode(bot.name));
      pos.appendChild(document.createTextNode("(" + bot.pos.x.toFixed(2) + "," + bot.pos.y.toFixed(2) + ")"));
      heading.appendChild(document.createTextNode("(" + bot.heading.x.toFixed(2) + "," + bot.heading.y.toFixed(2) + ")"));
      health.appendChild(document.createTextNode(bot.health));
      note.appendChild(document.createTextNode(bot.note));
      tr.appendChild(name);
      tr.appendChild(pos);
      tr.appendChild(heading);
      tr.appendChild(health);
      tr.appendChild(note);
      table.appendChild(tr);
    }
    document.getElementById('data').innerHTML = "";
    document.getElementById('data').appendChild(table);
  }
}
window.onload = initSSE;

