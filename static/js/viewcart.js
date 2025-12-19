async function loadCart() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        window.location.replace("/login");
        return;
    }

    const response = await fetch("/api/cart/view", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (!response.ok) {
        alert("Failed to load cart");
        return;
    }

    const data = await response.json();

    const container = document.getElementById("cart-items");
    const totalEl = document.getElementById("cart-total");

    container.innerHTML = "";

    if (data.items.length === 0) {
        container.innerHTML = "<p>Your cart is empty.</p>";
        totalEl.innerText = "0";
        return;
    }

    let total = 0;

    data.items.forEach(item => {
        total += item.subtotal;

        container.innerHTML += `
            <div class="item">
                <img src="${item.thumbnail}" alt="">
                <div>
                    <h4>${item.title}</h4>
                    <p>Price: ₹ ${item.price}</p>
                    <p>Quantity: ${item.quantity}</p>
                    <p><b>Subtotal:</b> ₹ ${item.subtotal}</p>
                </div>
            </div>
        `;
    });

    totalEl.innerText = total.toFixed(2);
}

document.addEventListener("DOMContentLoaded", loadCart);
