var curYPos = 0,
    curXPos = 0,
    curDown = false;

window.addEventListener('mousemove', function(e){ 
	if(curDown === true){
		window.scrollTo(document.body.scrollLeft + (curXPos - e.pageX), document.body.scrollTop + (curYPos - e.pageY));
	}
});

window.addEventListener('mousedown', function(e){ 
	curDown = true; 
	curYPos = e.pageY; 
	curXPos = e.pageX;

	var el = document.getElementsByClassName("sqlv-svg");
	el[0].setAttribute("class", "sqlv-svg sqlv-svg-grabing");
});

window.addEventListener('mouseup', function(e){ 
	curDown = false;
	var el = document.getElementsByClassName("sqlv-svg");
	el[0].setAttribute("class", "sqlv-svg");
});