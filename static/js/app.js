function addProduct() {
    fetch("/add", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: 1,
            name: "Soap",
            price: 30,
            qty: 10
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            loadProducts();
        });
}


function loadProducts() {
    fetch("/products")
        .then(res => res.json())
        .then(data => {
            const table = document.getElementById("productTable");
            table.innerHTML = "";

            data.forEach(p => {
                table.innerHTML += `
                <tr>
                    <td>${p.id}</td>
                    <td>${p.name}</td>
                    <td>${p.price}</td>
                    <td>${p.qty}</td>
                    <td>
                        <button onclick="sellProduct(${p.id})">Sell</button>
                        <button onclick="restockProduct(${p.id})">Restock</button>
                        <button onclick="deleteProduct(${p.id})">Delete</button>
                    </td>
                </tr>`;
            });
        });
}


function sellProduct(id) {
    fetch("/sell", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, qty: 1 })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            loadProducts();
        });
}


function restockProduct(id) {
    fetch("/restock", {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, qty: 5 })
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            loadProducts();
        });
}


function deleteProduct(id) {
    fetch(`/delete/${id}`, {
        method: "DELETE",
        credentials: "include"
    })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            loadProducts();
        });
}