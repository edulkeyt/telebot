$(document).ready(function(){

    var logControls = $(".log-control");

    logControls.each(function(index, item){

        var logControl = $(item);

        var textArea = logControl.find("textarea.log-text");

        var clearButton = logControl.find("button.log-clear-button");

        clearButton.click(function(){
            textArea.val("");
        });
    })    
})