function add_to_card(product_id) {

    console.log(`Ishladi, ${product_id}`)


    var url = `/shop/maishiytexnika/`;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': product_id
        })
    })
        .then((response) => {
            response.json().then((data) => {
                if (data['data'] != 'ok') {
                    alert(data['data'])
                }
            })
        })
}


function savatcha_change(soni, product_id){

    if (1<=soni<=5){
        console.log(soni, product_id)
    var url = `/cart/`;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'product_id': product_id,
            'soni':soni
        })
    })
        .then((response) => {
            response.json().then((data) => {
                if (data['data']!='ok'){
                    alert(data['data'])
                }
                else {
                    console.log(data['total_amount'])
                document.getElementById(`totalamount_${product_id}`).innerText= data['total_amount']
                }
            })
        })


    }

}


function savatcha(id) {
    soni = document.getElementById(`savatcha_${id}`).value
    console.log(soni)
    if (soni > 5) {
        alert("Siz beshtadan ortiq mahsulot kirata olmasiz")
        document.getElementById(`savatcha_${id}`).value=5
    }
    else if (soni<1){
        alert("Siz bittadan kam mahsulot kirita olmaysiz")
        document.getElementById(`savatcha_${id}`).value=1
    }
    else {
        savatcha_change(soni, id)
    }
}


function plus(id){
    soni = parseInt(document.getElementById(`savatcha_${id}`).value)
    console.log(soni)
    if (soni<=4 && soni>=1){
        document.getElementById(`savatcha_${id}`).value = soni+1
    }
    else {
        alert("noto'gri raqam")
    }
}