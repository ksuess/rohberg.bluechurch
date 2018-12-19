function dorenderpdf(url, canvasid) {
    // Asynchronous download of PDF
    var loadingTask = pdfjsLib.getDocument(url);
    loadingTask.promise.then(function(pdf) {
      console.log('PDF loaded');

      // Fetch the first page
      var pageNumber = 1;
      pdf.getPage(pageNumber).then(function(page) {
        console.log('Page loaded');

        var scale = 0.5;
        var viewport = page.getViewport(scale);

        // Prepare canvas using PDF page dimensions
        var canvas = document.getElementById(canvasid);
        var context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Render PDF page into canvas context
        var renderContext = {
          canvasContext: context,
          viewport: viewport
        };
        var renderTask = page.render(renderContext);
        renderTask.then(function () {
          console.log('Page rendered');
        });
      });
    }, function (reason) {
      // PDF loading error
      console.error(reason);
    });
};


$(document).ready(function() {

    // Loaded via <script> tag, create shortcut to access PDF.js exports.
    // var pdfjsLib = window['pdfjs-dist/build/pdf'];
    // var pdfjsLib = window['pdfjs-dist/build/pdf'];
    // console.debug(pdfjsLib);
    // webpack://pdfjs-dist/build/pdf/src/pdf.js
    //
    // // The workerSrc property shall be specified.
    pdfjsLib.GlobalWorkerOptions.workerSrc = '++theme++bluechurch/js/pdfjs/pdf.worker.js';

    // Link to PDF
    $("a[href$='.pdf']").each(function(index) {
        let url = $(this).attr("href");
        let canvasid = 'canvas-'+index;
        $(this).prepend("<canvas id='"+ canvasid +"'></canvas><br/>");
        dorenderpdf(url, canvasid);
        $(this).attr("target", "_blank");
    });


});
