function httpGetAsync(theUrl, callback) {
	
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() { 
	
		if(xmlHttp.readyState == 4 && xmlHttp.status == 200){
	
			console.log("response: " + theUrl);
		
			if (callback != null ){
				callback(xmlHttp.responseText);
			}
		}
	}
	
	console.log("request: " + theUrl);
	xmlHttp.open("GET", theUrl, true);
	xmlHttp.send(null);
}

var sendRequests = true;
function httpGetSync(url, callback){
	const _responseTimeout = 100;

	if(!sendRequests) return;
	sendRequests = false;
				
	function allowSendRequest(){sendRequests = true;}
				
	var timer = setTimeout(allowSendRequest, _responseTimeout);				
	httpGetAsync(url, function(httpResponse){
		clearTimeout(timer);
		allowSendRequest();
		if(callback != null){
			callback(httpResponse);
		}
	});
}
				
function getUrlCommand(command){
	return window.location.origin + "/" + command;
}