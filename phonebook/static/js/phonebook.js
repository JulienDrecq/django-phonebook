// JavaScript PhoneBook
// Author: Julien DRECQ

$('.lang-select').change(function() {
    $('.set-lang').submit();
});

// JS Table Filter simple insensitive
// url: http://bootsnipp.com/snippets/featured/js-table-filter-simple-insensitive
$(document).ready(function() {
    var activeSystemClass = $('.list-group-item.active');

    //something is entered in search form
    $('.system-search').keyup( function() {
       var that = this;
        // affect all table rows on in systems table
        var tableBody = $('.table-list-search tbody');
        var tableRowsClass = $('.table-list-search tbody tr');
        $('.search-sf').remove();
        tableRowsClass.each( function(i, val) {

            //Lower text for case insensitive
            var rowText = $(val).text().toLowerCase();
            var inputText = $(that).val().toLowerCase();
            if(inputText != '')
            {
                $('.search-query-sf').remove();
                var searching = gettext('Searching for:');
                tableBody.prepend('<tr class="search-query-sf"><td colspan="6"><strong>'+searching+' "'
                    + $(that).val()
                    + '"</strong></td></tr>');
            }
            else
            {
                $('.search-query-sf').remove();
            }

            if( rowText.indexOf( inputText ) == -1 )
            {
                //hide rows
                tableRowsClass.eq(i).hide();

            }
            else
            {
                $('.search-sf').remove();
                tableRowsClass.eq(i).show();
            }
        });
        //all tr elements are hidden
        if(tableRowsClass.children(':visible').length == 0)
        {
            var no_entries = gettext('No entries found.');
            tableBody.append('<tr class="search-sf"><td class="text-muted" colspan="6">'+no_entries+'</td></tr>');
        }
    });
});