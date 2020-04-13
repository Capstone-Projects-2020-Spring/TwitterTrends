const cloud_img_id = "word-cloud";

$(document).ready(function(){

    //alert("Enter a username and pick a network size and hit the button to generate a word cloud!");

    document.getElementById('update-graph-btn').addEventListener('click', function () {
        // example URL /wordcloud?username=Drake&count=8&depth=1
        const svgPresent = !! document.getElementById(cloud_img_id);
        if (svgPresent) {
            document.getElementById(cloud_img_id).remove();
        } else {
            document.getElementById('cloud-intro').remove();
        }
        let wordCloudURL = 'http://18.214.197.203:5000/wordcloud?username=';
        let uname = document.getElementById('search-cloud').value;
        let netCount = document.getElementById('drop-list-cloud').value;

        if (!uname || uname === ''){
            alert("Must enter a Username!")
        } else {
            alert("Hang on a moment while we generate a word cloud from " + uname + "'s network's content");
            wordCloudURL += uname + '&count=' + netCount + '&depth=1';
            // alert(wordCloudURL); // check that the url is correct
            let img = document.createElement('img');
            img.id = cloud_img_id;
            img.src = wordCloudURL;
            document.getElementById("cloud-div").appendChild(img);
        }
    });
});