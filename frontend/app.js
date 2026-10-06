async function checkHealth() {
    try {
        const response = await fetch("/api/health");
        const data = await response.json();

        document.getElementById("api-status").textContent = "Connected";

        if (data.database === "connected") {
            document.getElementById("db-status").textContent = "Connected";
        } else {
            document.getElementById("db-status").textContent = "Disconnected";
        }

    } catch (error) {
        document.getElementById("api-status").textContent = "Disconnected";
        document.getElementById("db-status").textContent = "Unknown";
    }
}


async function loadOrders() {
    const table = document.getElementById("orders-table");

    try {
        const response = await fetch("/api/orders");
        const orders = await response.json();

        table.innerHTML = "";

        let placed = 0;
        let shipped = 0;
        let delivered = 0;

        orders.forEach(order => {

            if (order.status === "PLACED") {
                placed++;
            }

            if (order.status === "SHIPPED") {
                shipped++;
            }

            if (order.status === "DELIVERED") {
                delivered++;
            }

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${order.id}</td>
                <td>${order.customer}</td>
                <td>${order.item}</td>
                <td>${order.quantity}</td>
                <td class="status">${order.status}</td>
            `;

            table.appendChild(row);
        });

        document.getElementById("total-orders").textContent = orders.length;
        document.getElementById("placed-orders").textContent = placed;
        document.getElementById("shipped-orders").textContent = shipped;
        document.getElementById("delivered-orders").textContent = delivered;

    } catch (error) {

        table.innerHTML = `
            <tr>
                <td colspan="5">Unable to load orders</td>
            </tr>
        `;
    }
}


async function initializeDashboard() {
    await checkHealth();
    await loadOrders();
}


initializeDashboard();
