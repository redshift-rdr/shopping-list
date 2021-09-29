
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
    var item_name = document.getElementById('add-item-name').value;
    var list_id = document.getElementById('list-id').value;

    // construct the http request
    var url = "api/items/add";
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && http.status == 200)
        {
            document.getElementById('add-item-name').value = '';
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
    http.send(JSON.stringify({ "list_id" : list_id, "name" : item_name }));
}

/* sends an http request to remove an item from current list
 * 
 * the list id is taken from 'list-id' input field and the item id
 * is taken from 'item-id' input field
 * 
 * Parameters
 * ----------
 * none
*/
function req_remove_item(button)
{
    // grab the list-id and item-id
    var list_id = document.getElementById('list-id').value;
    var item_id = button.dataset.id;

    // construct the request
    var url = "api/items/remove";
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

    // open the request and set content type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // send the request
    http.send(JSON.stringify({ "list_id" : list_id, "item_id" : item_id }));
}

/* updates the item dropdown list
 * 
 * Parameters
 * ----------
 * items : array, required
 *    The items to put into the dropdown list
*/
function update_item_dropdown(items)
{
    var dropdown = document.getElementById("myDropdown");

    while (dropdown.firstChild) 
    {
        dropdown.removeChild(dropdown.lastChild);
    }

    for (item in items)
    {
        var link = document.createElement('a');
        var text = document.createTextNode(items[item]);

        link.appendChild(text);
        link.href='#';
        link.onclick = function() {
            document.getElementById('add-item-name').value = this.innerHTML;
        }
        dropdown.appendChild(link);
    }

    document.getElementById("myDropdown").classList.add("show");
}

function update_itemname_from_dropdown_click(link)
{

}

/* sends a http request to the api to retrieve items that begin with a given string
 * 
 * Parameters
 * ----------
 * none
*/
function req_get_matching_items()
{
    // grab the contents of the item name field
    var item_name = document.getElementById('add-item-name').value;

    // construct the request
    var url = "api/items/get";
    var http = new XMLHttpRequest();
    http.onreadystatechange = function()
    {
        // if the request finishes and is successful
        if (http.readyState == 4 && http.status == 200)
        {
            update_item_dropdown(JSON.parse(http.responseText));
        }
        else if (http.readyState == 4 && http.status != 200)
        {
            // log the error
            console.log(http.responseText);
        }
    };

    // open the request and set content type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // send the request
    http.send(JSON.stringify({ "match_string" : item_name }));
}

function req_make_item_recurring(button)
{
    // grab the list-id and item-id
    var item_id = button.dataset.id;

    // construct the request
    var url = "api/items/make_recurring";
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

    // open the request and set content type to JSON
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // send the request
    http.send(JSON.stringify({ "item_id" : item_id }));
}