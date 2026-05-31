document.addEventListener('DOMContentLoaded', () => {
    let total = 0;
    document.querySelectorAll('tbody tr').forEach(row => {
        const priceCell = row.querySelector('[data-label="Цена"]');
        const qtyCell = row.querySelector('input[name="quantity"]');
        if (priceCell && qtyCell) {
            const price = parseFloat(priceCell.textContent.replace(/[^\d.]/g, '')) || 0;
            const qty = parseInt(qtyCell.value) || 1;
            total += price * qty;
            // Обновляем сумму строки
            row.querySelector('[data-label="Сумма"]').textContent = `${(price * qty).toFixed(2)} ₽`;
        }
    });
    document.getElementById('cart-total').textContent = `${total.toFixed(2)} ₽`;
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}