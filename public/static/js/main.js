var FONT_MIN = 10;
var FONT_MAX = 80;


function getProba(inputText) {

    fetch('/get_proba', { method: "POST", body: inputText }).then(response => response.text().then(json_response => {
        response = JSON.parse(json_response)
        console.log(response);
        let maxCategory = '';
        let maxProba = 0;
        for (const[key, value] of Object.entries(response)){
            proba = parseFloat(value);
            if (proba > maxProba){
                maxCategory = key;
                maxProba = proba;
            }
            new_font_size = Math.ceil(FONT_MIN + ((FONT_MAX - FONT_MIN) * proba^2));
            console.log(new_font_size);
            $(`.${key}`).stop().animate({
                fontSize: `${new_font_size}px`
            }, 1000);
        }
        for (const[key, value] of Object.entries(response)){
            if (key == maxCategory){
                setTimeout($(`.${key}`).css('font-weight', 'bold'), 500)
            } else{
                setTimeout($(`.${key}`).css('font-weight', 'normal'), 500)
            }
            
        }
    }));
}


$(document).ready(function () {
    console.log("ready!");
    $('#input-area').bind('input propertychange', function () {
        getProba(this.value);
    });
});
