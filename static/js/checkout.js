const orderId = window.location.pathname.split("/").pop();

document.getElementById("pay-btn").addEventListener("click", async () => {
    const res = await fetch(`/api/payments?order_id=${orderId}`, {
        method: "POST"
    });

    if (!res.ok) {
        const errorData = await res.json();
        const errorType = errorData.detail;
        if (errorType === "Already Paid") {
        alert("Already Paid");
    }
    else{
        alert("Payment failed");}
        
    return;
    }
    alert("Payment successful");
    window.location.href = `/payment-success/${orderId}`;
});
