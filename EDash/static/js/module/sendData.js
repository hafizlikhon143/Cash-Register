function sendData(link, data, func){
    let fetchData = fetch(link, {
        method: data.method,
        headers: {
            'X-CSRFToken': data.token == undefined? "": data.token,
            'Content-Type': data.cont_type == undefined? 'application/json': data.cont_type
        },
        body: JSON.stringify(data.body)        
    })
    .then(res=>{return res.json()})
    .then(response=>{
        func(response);
    })
}