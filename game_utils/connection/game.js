//Setups up the game

const links = {};
var colour = {};

function init() {
    //position labels
    var countries = document.getElementById("map").querySelectorAll(".country");
    var x = {
        "AL": 20, 
        "CA": -65,
        "SF": -15,
        "NY": -15,
        "ME": -28,
        "GR": -10,
        "VE": -15,
        "BR": -10,
        "PE": -15,
        "AG": -20,
        "UK": 0,
        "RO": -5,
        "SC": 2,
        "PR": -12,
        "RU": -10,
        "NR": -10,
        "PL": -10,
        "UR": -20,
        "SI": -20,
        "AF": -5,
        "MI": -20,
        "IN": -17,
        "SE": -27,
        "JP": -7,
        "CH": -20,
        "PA": -12,
        "NA": -15,
        "EG": -10,
        "WA": -20,
        "CN": -18,
        "SA": -13,
        "MA": -15,
        "CO": 10,
        "WO": -10,
        "EO": -10,
        "NG": -10
    }
    var y = {
        "GR": -23,
        "AL": -15,
        "CA": -15,
        "SF": -15,
        "NY": -20,
        "ME": -30,
        "VE": -23,
        "BR": -23,
        "PE": -15,
        "AG": -30,
        "UK": -5,
        "RO": -20,
        "PR": -20,
        "SC": -25,
        "RU": -15,
        "SI": -3, 
        "PL": -20,
        "NR": -15,
        "UR": -22,
        "NA": -20,
        "WA": -30,
        "EG": -15,
        "CN": -15,
        "MA": -15,
        "SA": -15,
        "MI": -20,
        "AF": -25,
        "PA": -20,
        "IN": -15,
        "SE": -32,
        "CH": -20,
        "JP": -10,
        "NG": -15,
        "CO": -10,
        "WO": -10,
        "EO": -10
    }
    for (i=0; i<countries.length; i++) {
        var ID = countries[i].id;
        var original = document.getElementById(ID);
        var lab = document.getElementsByName(ID)[0];
        var w = 0;
        var h = 0;
        var dimensions = original.getBoundingClientRect();
        var width = dimensions["width"] 
        var height = dimensions["height"]
        var left = dimensions["left"]
        var top = dimensions["top"]
        w = x[ID]
        h = y[ID]
        lab.style.position = "absolute"
        lab.style.left = left + width/2 + w -100;
        lab.style.top = top + height/2 + h;
        lab.style.color = "#e8ecf1";
        lab.style.fontFamily = "sans-serif";
        lab.style.fontSize = 20;
        lab.style.fontWeight = 200;
    }
}

init();