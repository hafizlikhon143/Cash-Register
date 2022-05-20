var btn1 = document.querySelectorAll('.product_add_btn');

listEventListener(btn1, add_to_order, "click");

function add_to_order(e){
    let id = e.target.dataset.id;
    let inp = document.querySelector(`.product_inp_qty[data-id="${id}"]`).value;
    let order_val = document.querySelector(`.cart_form[data-id="${id}"]`).value;
    
    let res = sendData('/order_product', {
        method: "post",
        token: csrf_token,
        cont_type: "",
        body: {
            "qty": inp,
            "id": id,
            "order_id": order_val
        }
    }, get_val)
    inp.value = 0;
}


function get_val(val){
    let p_qty = document.querySelector('.p_qty[data-id="'+val.id+'"]>span');
    let msg_cont = document.querySelector("#p_msg");
    if(val.msg !=undefined){
        changeHtml(val.msg, msg_cont);
    }
    else if(val.p_qty != undefined){
        changeHtml(val.p_qty, p_qty);
        changeHtml("", msg_cont);
    }
    console.log(val);
}

// Add Click Event Listener to list of btns

function listEventListener(list, func, eventType){
    list.forEach(l=>l.addEventListener(eventType, func))
}

