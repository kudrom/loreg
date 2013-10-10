// Global variables
var wrapper = document.querySelector(".wrapper"),
    warning = document.querySelector(".warning"),
    close= document.querySelector(".close"),
    ORANGE = "#EF8E51",
    BLUE = "#829FE9";

// *************************** COMMON FUNCTIONS *******************************
//Transforms the coordinates of the dom element into the internal canvas
function windowToCanvas(x, y, canvas){
    var bbox = canvas.getBoundingClientRect();
    return {x: x-bbox.left * (canvas.width  / bbox.width),
            y: y-bbox.top  * (canvas.height / bbox.height)}
}

//Calculates the distance between two points
function dist(p1, p2){
    var dx = p1.x - p2.x,
        dy = p1.y - p2.y;
    return Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));
}

//Calculates the sum of the list given as argument
function sum(list){
    var acc = 0;
    for(var i = 0; i < list.length; i++){
        acc += list[i];
    }
    return acc;
}

// Calculates the minimum of a list
function min(list){
    var ret = list[0];
    for(var i = 1; i < list.length; i++){
        if(list[i] < ret){
            ret = list[i];
        }
    }
    return ret;
}

// Calculates the maximum of a list
function max(list){
    var ret = list[0];
    for(var i = 1; i < list.length; i++){
        if(list[i] > ret){
            ret = list[i];
        }
    }
    return ret;
}

function pretty_number(number){
    var n = String(number),
        ret = n.slice(-3);
    for(var i = 3; i < n.length; i += 3){
        ret = n.slice(-i - 3, -i) + "." + ret;
    }
    return ret
}

/* Updates the heights of every article to the height of the screen or the MIN_HEIGHT.
 * I've to update NAV_HEIGHT because of the responsive design
 */
function update_heights(MIN_HEIGHT, articles){
    var NAV_HEIGHT = nav ? nav.offsetHeight : 0,
        height = window.innerHeight > MIN_HEIGHT ? window.innerHeight - NAV_HEIGHT : MIN_HEIGHT;

    console.log(height, NAV_HEIGHT, nav);
    for (i = 0; i < articles.length; i++){
        articles[i].style.height = height + "px";
    }
}

//From the MDC
function get_random(min, max){
    return Math.floor(Math.random() * (max - min +1)) + min;;
}

function isCanvasSupported(){
      var elem = document.createElement('canvas');
      return !!(elem.getContext && elem.getContext('2d'));
}

function showWarning(){
    close.onclick = closeWarning;
    warning.classList.remove("hidden");
    nav.style.marginTop = warning.offsetHeight + 'px';
    wrapper.style.marginTop = (30 + warning.offsetHeight) + 'px';
    window.onresize = function(){
        nav.style.marginTop = warning.offsetHeight + 'px';
        wrapper.style.marginTop = (30 + warning.offsetHeight) + 'px';
    }
}

function closeWarning(){
    nav.style.marginTop = 0;
    wrapper.style.marginTop = '30px';
    warning.classList.add("hidden");
}

if(!isCanvasSupported()){
    showWarning();
}
