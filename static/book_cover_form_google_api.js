$(document).ready(function () {

    // Iterate through EACH element with the class '.book'
    $('.book').each(function () {
        // 'this' is now the current .book element in the loop
        var $bookElement = $(this);
        var isbn = $bookElement.data('isbn');

        // Find the specific .thumbnail element WITHIN the current .book
        var $thumbnailElement = $bookElement.find('.thumbnail');

        if (isbn) {
            // Execute the AJAX call for EACH ISBN separately
            $.ajax({
                dataType: 'json',
                url: 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn,

                // We use an anonymous function as a success handler,
                // which has access to the specific elements ($thumbnailElement).
                success: function (response) {
                    handleBookApiResponse(response, $thumbnailElement);
                },
                error: function () {
                    $thumbnailElement.attr('alt', 'Error loading cover art.');
                }
            });
        }
    });
});

/**
 * Processes the API response and updates ONLY the passed thumbnail element.
 * @param {object} response - The JSON response from the Google Books API.
 * @param {jQuery} $specificThumbnail - The specific <img> element to be updated.
 */
function handleBookApiResponse(response, $specificThumbnail) {
    if (response.items && response.items.length > 0) {
        var item = response.items[0];

        if (item.volumeInfo.imageLinks && item.volumeInfo.imageLinks.thumbnail) {
            var thumb = item.volumeInfo.imageLinks.thumbnail;

            // Important: We use $specificThumbnail, NOT $('.thumbnail')
            $specificThumbnail.attr('src', thumb);
            $specificThumbnail.attr('alt', item.volumeInfo.title + ' Cover');
        } else {
            $specificThumbnail.attr('alt', 'No image available.');
        }
    } else {
        $specificThumbnail.attr('alt', 'No results found.');
    }
}