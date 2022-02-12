var FONT_MIN = 10;
var FONT_MAX = 80;


function updateProba(inputText) {

    fetch('/get_proba', { method: "POST", body: inputText }).then(response => response.text().then(json_response => {
        response = JSON.parse(json_response);
        let maxCategory = '';
        let maxProba = 0;
        for (const[key, value] of Object.entries(response)){
            proba = parseFloat(value);
            probaPercent = `${(proba * 100).toFixed(2)}%`
            if (proba > maxProba){
                maxCategory = key;
                maxProba = proba;
            }
            new_font_size = Math.ceil(FONT_MIN + ((FONT_MAX - FONT_MIN) * proba^2));
            // Populate tooltips with percentage probabilities
            $(`.${key}`).find(">:first-child").text(probaPercent)
            // Adjust font sizes to reflect relative probabilities of categories
            $(`.${key}`).stop().animate({
                fontSize: `${new_font_size}px`
            }, 1000);
        }
        // Make text for category with highest probability bold
        for (const[key, value] of Object.entries(response)){
            if (key == maxCategory){
                $(`.${key}`).delay(500).css('font-weight', 'bold')
            } else{
                $(`.${key}`).delay(500).css('font-weight', 'normal')
            }
        }
    }));
}

function writePageInfo(){
    $.getJSON('static/json/model_info.json', function(modelInfo){
        pageInfo =
            `Probabilities are from a Naive Bayes classifier trained ` +
            `on a balanced sample of ${modelInfo['num_train_files']} articles ` +
            `from the BBC News website that achieved ${modelInfo['accuracy_percent']} ` +
            `accuracy when tested on a sample of ${modelInfo['num_test_files']} articles. ` +
            `Paste an article from BBC News or another news source, or simply type a few words ` +
            `into the text area below to try the model out for yourself.`
        $('#page-info').text(pageInfo)
    })
}


$(document).ready(function () {
    writePageInfo()
    // Update probability display whenever input area text changes
    $('#input-area').bind('input propertychange', function () {
        updateProba(this.value);
    });
});
