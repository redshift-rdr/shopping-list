
/* closes the dropdown when user clicks anywhere 
*/
window.onclick = function(event) 
{
    if (!event.target.matches('.dropbtn')) 
    {
        var dropdown = document.getElementById("myDropdown");
        if (dropdown.classList.contains('show')) 
        {
            dropdown.classList.remove('show');
        }
    }
} 

/* sends a http request to add an item to the current list
 *
 * the item name is taken from the 'add-item-name' input field
 * and the data is sent as JSON. If the request is successful it
 * forces the page to reload.
 * 
 * Parameters
 * ----------
 * none
*/ 
function req_add_item()
{
    // grab the required values from the input fields
    var name = document.getElementById('name_input').value;
    var brand = document.getElementById('brand_input').value;
    var quantity = document.getElementById('qty_input').value;
    var link = document.getElementById('link_input').value;
    var note = document.getElementById('note_input').value;
    var requestor = document.getElementById('requestor_input').value;

    // construct the http request
    var url = "/items/add";
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && http.status == 200)
        {
            document.getElementById('name_input').value = '';
            document.getElementById('brand_input').value = '';
            document.getElementById('qty_input').value = '';
            document.getElementById('link_input').value = '';
            document.getElementById('note_input').value = '';
            document.getElementById('requestor_input').value = '';

            // refresh the page to show the newly added item
            location.reload();
        }
        else if (http.readyState == 4 && http.status != 200)
        {
            // log the error
            console.log(http.responseText);
        }
    };

    // open the request, and set the data type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // send off the request
    http.send(JSON.stringify({ "name" : name, "brand" : brand, "quantity" : quantity, "link": link, "note": note, "requestor": requestor }));
}

function clear_list()
{
    // construct the http request
    var url = "/items/clear";
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && http.status == 200)
        {

            // refresh the page to show the newly added item
            location.reload();
        }
        else if (http.readyState == 4 && http.status != 200)
        {
            // log the error
            console.log(http.responseText);
        }
    };

    // open the request, and set the data type to JSON
    http.open("GET", url);

    // send off the request
    http.send();
}