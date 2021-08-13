
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
    var item_name = document.getElementById('add-item-name').value;
    var list_id = document.getElementById('list-id').value;

    // construct the http request
    var url = "api/items/add";
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && request.status == 200)
        {
            // refresh the page to show the newly added item
            location.reload();
        }
        else if (http.readyState == 4 && request.status != 200)
        {
            // log the error
            console.log(http.responseText);
        }
    };

    // open the request, and set the data type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // send off the request
    http.send(JSON.stringify({ "list_id" : list_id, "name" : item_name }));
}