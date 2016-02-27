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

function initSSE(){
  document.getElementById('loading').style.visibility="visible";
  document.getElementById('pbar').style.visibility="visible";
  var source = new EventSource("/cgi-bin/koth/redis-relay.cgi?world=" + document.getElementById('channel-txt').value);
  source.onopen = function(event){
    window.setInterval(incrementTimeCount, timedelay);
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
    var cols = ["name","position","heading","health","recharge","note"]
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
      var recharge = document.createElement('td');
      var note = document.createElement('td');
      name.appendChild(document.createTextNode(bot.name));
      pos.appendChild(document.createTextNode("(" + bot.pos.x.toFixed(2) + "," + bot.pos.y.toFixed(2) + ")"));
      heading.appendChild(document.createTextNode("(" + bot.heading.x.toFixed(2) + "," + bot.heading.y.toFixed(2) + ")"));
      health.appendChild(document.createTextNode(bot.health));
      recharge.appendChild(document.createTextNode(bot.rechargeTime));
      note.appendChild(document.createTextNode(bot.note));
      tr.appendChild(name);
      tr.appendChild(pos);
      tr.appendChild(heading);
      tr.appendChild(health);
      tr.appendChild(recharge);
      tr.appendChild(note);
      table.appendChild(tr);
    }
    document.getElementById('data').innerHTML = "";
    document.getElementById('data').appendChild(table);
  }
}
window.onload = function(){
  document.getElementById('loading').style.visibility = "hidden";
}

