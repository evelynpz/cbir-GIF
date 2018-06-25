/*
Norwegian University of Science and Technology
Content-based Indexing and Retrieval
Project: GIF Image Retrieval in Cloud Computing Environment
Partners: Evelyn Paiz & Nadile Nunes
Instructor: Sule Yildirim
Description: Main js.
Ref: https://www.pyimagesearch.com/2014/12/08/adding-web-interface-image-search-engine-flask/
*/

// Hide initial
$("#searching").hide();
$("#results-table").hide();
$("#error").hide();
 
// Global
var url = 'dataset/';
var data = [];
var time = 0;
 
$(function() {
 
    // Sanity check
    console.log( "ready!" );

    // Image click
    $(".img").click(function() {

        // Empty/hide results
        $("#results").empty();
        $("#results-table").hide();
        $("#error").hide();
        $("#time").empty();
        $("#time").hide();
        
        // Remove active class
        $(".img").removeClass("active")

        // Add active class to clicked picture
        $(this).addClass("active")

        // Grab image url
        var image = $(this).attr("src")
        console.log(image)

        // Show searching text
        $("#searching").show();
        console.log("searching...")

        // Ajax request
        $.ajax({
            type: "POST",
            url: "/search",
            data : { img : image },
            // Handle success
            success: function(result) {
                console.log("time: "+result.time)
                console.log(result.results);
                var data = result.results
                var time = result.time
                // Loop through results, append to dom
                for (i = 0; i < data.length; i++) {
                    $("#results").append('<tr><th><a href="'+url+data[i]["image"]+'"><img src="'+url+data[i]["image"]+'" class="result-img"></a></th><th>'+data[i]['score']+'</th></tr>')
                };
                // Apend the time of search
                $('#time').append('Search complete! elapsed time: '+time+' ms')
                // Show results and hide searching text
                $("#searching").hide();
                $("#time").show();
                $("#results-table").show();
            },
            // handle error
            error: function(error) {
                console.log(error);
                // append to dom
                $("#error").append()
            }
        });
        
    });
 
});