var globalEventMapping = {},
	globalManagerMapping = {},
	globalCallerMapping = {};

// binds an event with the appropriate handler
function bind(canvas, event, cobj, caller){
	// Handle the event with the global manager to bind the proper manager to the cobj
	canvas["on"+event] = globalEventHandler;
	if(!(canvas.className in globalEventMapping)){
		globalEventMapping[canvas.className] = new Object();
		globalEventMapping[canvas.className][event] = cobj;

		// Avoid the TypeError exception in the manager filling the dictionary with a undefined
		globalCallerMapping[canvas.className] = new Object();
	}else{
		globalEventMapping[canvas.className][event] = cobj;
	}
	if(caller !== undefined){
		globalCallerMapping[canvas.className][event] = caller;
	}
}

/* I've to supply this global manager because in the event binding 
 * (DOMElement.onmousedown) the handler (in this case globalEventHandler, see the function bind)
 * is binded with the DOM element that binded it and i can't access the 
 * "complex object" through "this" in this handler, so i have to bind the primitive
 * event to a proxy (globalEventHandler) in order to call the real handler 
 * (the manager) with the complex object so it can update the state of the canvas.
 */
function globalEventHandler(e){
	var manager = globalManagerMapping[e.type],
		cobj = globalEventMapping[this.className][e.type];
	manager.call(cobj, e, this);
}

// Manager for click events
function clickHoverHandler(e, canvas){
	var loc = windowToCanvas(e.clientX, e.clientY, canvas),
		context = canvas.getContext("2d"),
		BckgCanvas = document.createElement("canvas"),
		BckgContext = BckgCanvas.getContext("2d"),
		i, length = this.objects.length,
		mouseout = true,
		caller = globalCallerMapping[canvas.className][e.type],
		args,
		func = {"mousedown": this.mdown, "mousemove": this.mover,
				"mouseout": this.mout, "mouseup": this.click};
	
	// Iterate over the objects
	for(i = 0; i < length; i++){
		this.objects[i].build_path(BckgContext);
		if(BckgContext.isPointInPath(loc.x, loc.y)){
			// Call the handler of the object
			canvas.style.cursor = "pointer";
			args = [this.objects[i], canvas];
			if(caller !== undefined){
				args.push(caller);
				e.stopPropagation();
			}
			func[e.type].apply(this, args);
			mouseout = false;
			break;
		}
	}
	// the mouse is out of any object
	if(mouseout){
		canvas.style.cursor = "default";
		args = [this.objects[i], canvas];
		if(caller !== undefined){
			args.push(caller);
			e.stopPropagation();
		}
		func["mouseout"].apply(this, args);
	}
}
// register the manager with the proper event types
globalManagerMapping["mouseup"] = clickHoverHandler;
globalManagerMapping["mousedown"] = clickHoverHandler;
globalManagerMapping["mousemove"] = clickHoverHandler;