
function req_add_item()
{
    var item_name = document.getElementById('add-item-name').value;
    var list_id = document.getElementById('list-id').value;

    var http = XMLHttpRequest();
    var url = "api/items/add";
    var headers = "Content-Type: application/json";
    http.open("POST", url);
    http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    http.send(JSON.stringify({ "list_id" : list_id, "name" : item_name }));
}