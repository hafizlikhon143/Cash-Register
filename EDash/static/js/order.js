if(window.location.pathname.search("products/") == 1) {
    var orderForm = document.querySelector(".cart_form_2");
    var csrf_token = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    orderForm.addEventListener("change", getData);
    
    function getData(e){
        // Fetching The Cart Data
        if(e.target.value !== "none"){
            var data = fetch("/order_data/"+e.target.value, {
                method: "get",
            })
            .then(res=>{return res.json()})
            .then(r=>{
                var orderTable = document.querySelector("#order_table");
                // Genrate Table element
                orderTable.innerHTML = createElem(r);
                // Increament and Decreament of Product on Btn Click
                dltCart();
                inCart();
                stateCart();
            })
        }
        else{
            var orderTable = document.querySelector("#order_table");
    
            orderTable.innerHTML = "<tr><td>Nothing Selected Yet</td></tr>";
        }
    }
    
    
    function stateCart(){
        var stateBtn = document.querySelectorAll('.cstatusBtn')
        if(stateBtn !== undefined){
            stateBtn.forEach(btn=>{
                btn.addEventListener("click", changeStatus)
            })
        }
    }
    
    function inCart(){
        var cartInbtn = document.querySelectorAll('.caddBtn')
    
        if(cartInbtn !== undefined){
            cartInbtn.forEach(btn=>{
                btn.addEventListener('click', inAction);
            })
        }
    }
    
    function dltCart(){
        var cartDbtn = document.querySelectorAll(".cdltBtn");
        
        if(cartDbtn !== undefined){
            cartDbtn.forEach(btn=>{
                btn.addEventListener('click', dltAction);
            })
        }
    }
    
    // Genrate Table element
    function createElem(r){
        let elem = '';
        if (r.obj === false){
            elem += "<td colspan='6' style='text-align: center'>There is no product added yet!!</td>";
        }
        else{
            for(i=0;i<r.obj.length;i++){
                elem = elem + `<tr data-id="${r.obj[i].id}">
                    <td>${r.obj[i].name}</td>
                    <td>${r.obj[i].catagory}</td>
                    <td class="order_qty" data-id='${r.obj[i].id}'>${r.obj[i].qty}</td>
                    <td>${r.obj[i].m_price}</td>
                    <td>${r.obj[i].retail}</td>
                    <td class="cart_action">
                        <button class="cdltBtn btn btn-primary" data-id="${r.obj[i].id}" data-p_qty="${r.obj[i].p_qty}" data-cart='${r.obj[i].cart}'><</button>
                        <button class="caddBtn btn btn-primary" data-id="${r.obj[i].id}" data-p_qty="${r.obj[i].p_qty}" data-cart='${r.obj[i].cart}'>></button>
                        <button class="cstatusBtn btn btn-danger" data-id="${r.obj[i].id}" data-p_qty="${r.obj[i].p_qty}" data-cart="${r.obj[i].cart}">Complete</button>
                    </td>
                </tr>`;
            }
        }
        return elem;
    }
    
    // Event Change Status of Order
    
    function changeStatus(e){
        let product_id = e.target.dataset.id;
        let cart_id = e.target.dataset.cart;
        if(confirm("Are you sure you want to complete order") == true){
            let change_data = sendData("/order_data/"+cart_id, {
                method: "post",
                token: csrf_token,
                cont_type: "",
                body: {
                    status: true,
                    target: product_id,
                    func: "change_status"
                }
            }, statusFunc)
        }
    }
    
    function statusFunc(val){
        window.location.reload();
    }
    
    // Event button Increament function
    function inAction(e){
        let product_id = e.target.dataset.id;
        let cart_id = e.target.dataset.cart;
        let order_qty = document.querySelector(`.order_qty[data-id="${product_id}"]`)
        let product_qty = order_qty.dataset.p_qty;
        if(product_qty != 1){
            djFetch('/order_data/'+cart_id, {'target': product_id, 'func': "add"}, order_qty, product_qty);
        }
        else if(confirm("Are you sure you want to add whole stock")){
            djFetch('/order_data/'+cart_id, {'target': product_id, 'func': "add"}, order_qty, product_qty);
        }
        else{
            window.location.reload();
        }
    
    }
    
    // Event button Decreament function
    function dltAction(e){
        let product_id = e.target.dataset.id;
        let cart_id = e.target.dataset.cart;
        let order_qty = document.querySelector(`.order_qty[data-id="${product_id}"]`)
        let product_qty = document.querySelector(`.p_qty[data-id="${product_id}"]`)
        if(order_qty.innerHTML != 1){
            djFetch('/order_data/'+cart_id, {'target': product_id, 'func': "del"}, order_qty, product_qty);
        }
        else if(confirm("Are you sure you want to delete it")){
            let tr = document.querySelector(`tr[data-id="${product_id}"]`)
            tr.style.display = "none";
            djFetch('/order_data/'+cart_id, {'target': product_id, 'func': "del"}, order_qty, product_qty);
        }
        else{
            window.location.reload();
        }
    
    }
    
    
    // Dlt Function
    function djFetch(link, val, t1, t2){
        fetch(link, {
            method: 'post',
            headers: {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(val)
        })
        .then(res=>{return res.json()})
        .then(r=>{
            changeHtml(r.qty, t1);
        });
    }
    
    // Target Html And Change its content
    function changeHtml(val, target){
        target.innerHTML = val;
    }
}