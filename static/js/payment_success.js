const orderId = window.location.pathname.split("/").pop();

async function validatePayment() {
    const res = await fetch(`/api/payments/success/${orderId}`);

    if (!res.ok) {
        const errorData = await res.json();

        if (errorData.detail === "Order not found") {
            alert("Invalid order ID");
        } else {
            alert("Payment not completed");
        }

        window.location.href = "/orders";
        return;
    }

    
}

validatePayment();
