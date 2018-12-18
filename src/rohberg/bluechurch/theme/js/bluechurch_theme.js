$(document).ready(function() {

    // "related item" als audio player anzeigen, wenn mp3 oder aehnliches
    var extensions = ["mp3", "mp4", "wma", "wav", "m4a", "m4b", "mpc", "aiff"];
    // "m4p",
    for (i = 0; i < extensions.length; i++) {
        var related_audio = $('.relatedItems a[href$="'+ extensions[i] +'"]').each(function( index ) {
            var filename = "/"+$(this).attr('href').split("/").slice(3).join("/");
            $(this).parent().html($(this).html() +'<br><audio src="'+ filename +'" controls="controls"></audio>');
        });
    } ;

    // Links auf Audio-Files in Player umwandeln
    var extensions = ["mp3", "mp4", "wma", "wav", "m4a", "m4b", "mpc", "aiff"];
    // "m4p",
    var snip = '<audio src="mysrc" controls="controls"></audio>'
    for (i = 0; i < extensions.length; i++) {
        $("body").not("body.template-file_view")
            .find('a[href$=".' + extensions[i] + '"]').each(function() {
                var href = $(this).attr('href');
                // $(this).parent().html(snip.replace('mysrc',href));
                $(this).replaceWith(snip.replace('mysrc',href));
        })
    } ;


    // collective.collectionfilter
    // replace - with space
    $('.filterLabel').each(function(index) {
        var txt = $(this).text();
        $(this).text(txt.replace(/-/g, " "));
    });


    $("label[for='__ac_name'], label[for='userid']").text("Email");

    // Translations
    // $("html[lang='de']");
    $("html[lang='de'] label[for='form-widgets-ILeadImage-image']").text("Profilbild");
    $("html[lang='de'] label[for='form-widgets-ILeadImage-image_caption']").text("Legende zum Profilbild");


    // Portlets collapsed. Header rausnehmen, damit sichtbar
    var portlet = $("aside.filterCity, aside.filterCountry");
    portlet.each(function() {
        var pwrapper = $(this).parent().addClass("portletWrapperCollapsible");
        var pheader = $(this).find(".portletHeader");
        $(this).wrap( "<div class='innerPortletwrapper'></div>" );
        var iwrapper = pwrapper.find(".innerPortletwrapper");
        pheader.addClass("portletHeaderCollapsible").insertBefore(iwrapper);

        pheader.click(function() {
          iwrapper.slideToggle( function() {
            // Animation complete.
          });
        });
    });


    // Playlist play button
    $("a.playlist-button").click(function() {
        window.open(this.href, "_blank", "width=500,height=600");
        return false;
    });


    // Menu on small devices
    $( ".plone-navbar-toggle" ).click(function(event) {
        var pnt = $(this);
        event.stopPropagation();
        var target = $(this).attr('data-target');
        $(target).slideToggle( "slow", function() {
            pnt.toggleClass("expanded");
        });
    });


    var piep = "piep piep zwitscher";
    // console.log(piep);
});
