let shoppingCart = [];

// Inicialización del Carrito al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const savedCart = localStorage.getItem('retropulse_cart');
    if (savedCart) {
        try {
            shoppingCart = JSON.parse(savedCart);
        } catch (e) {
            shoppingCart = [];
        }
    }
    updateCartBadge();
    
    // Si el usuario se encuentra en la página de resumen del carrito, se renderiza
    if (document.getElementById('cart-items-container')) {
        renderCartPage();
    }
});

// Actualiza el indicador numérico del carrito en el navbar
function updateCartBadge() {
    const totalCount = shoppingCart.reduce((sum, item) => sum + item.quantity, 0);
    const badge = document.getElementById('cart-badge');
    if (badge) {
        badge.innerText = totalCount;
    }
}

// Agregar producto con cantidad variable al carrito desde la página de detalles
function addToCartGlobal(cod, nombre, precio, imgUrl, qty, maxStock) {
    const exist = shoppingCart.find(item => item.cod_producto === cod);
    
    if (exist) {
        const projectedQty = exist.quantity + qty;
        if (projectedQty <= maxStock) {
            exist.quantity = projectedQty;
            showNotificationToast(`Se agregaron ${qty} unidades de ${nombre} al carrito.`);
        } else {
            showNotificationToast(`No puedes agregar más unidades. El stock en la bóveda es de ${maxStock}.`, true);
            return;
        }
    } else {
        shoppingCart.push({
            cod_producto: cod,
            nombre: nombre,
            precio: parseFloat(precio),
            imagen_url: imgUrl,
            quantity: qty
        });
        showNotificationToast(`Se agregaron ${qty} unidades de ${nombre} al carrito.`);
    }

    localStorage.setItem('retropulse_cart', JSON.stringify(shoppingCart));
    updateCartBadge();
}

// Renderizado reactivo dentro de cart.html
function renderCartPage() {
    const container = document.getElementById('cart-items-container');
    if (!container) return;
    
    container.innerHTML = '';

    if (shoppingCart.length === 0) {
        container.innerHTML = `
            <div class="bg-cyber-card rounded-xl p-12 text-center border border-cyber-purple/30">
                <i class="fa-solid fa-ghost text-5xl text-cyber-pink/60 mb-4 block"></i>
                <p class="text-lg font-retro text-slate-400">Tu carrito se encuentra vacío de reliquias.</p>
                <a href="/catalogo/" class="mt-4 inline-block px-6 py-2 border-2 border-cyber-cyan text-cyber-cyan font-retro font-bold rounded hover:bg-cyber-cyan/10 transition">EXPLORAR VAULT</a>
            </div>
        `;
        updateBillTotals(0);
        return;
    }

    shoppingCart.forEach((item, index) => {
        const subtotalItem = item.precio * item.quantity;
        container.innerHTML += `
            <div class="bg-cyber-card p-5 rounded-xl border border-cyber-purple/30 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="flex items-center gap-4 w-full sm:w-auto">
                    <img src="${item.imagen_url}" alt="${item.nombre}" class="w-16 h-16 object-cover rounded border border-cyber-pink/30">
                    <div>
                        <h4 class="font-bold text-white text-lg">${item.nombre}</h4>
                    </div>
                </div>

                <div class="flex items-center justify-between sm:justify-end gap-6 w-full sm:w-auto">
                    <!-- Control de cantidades -->
                    <div class="flex items-center border border-cyber-purple/50 rounded overflow-hidden">
                        <button onclick="changeCartQty(${index}, -1)" class="px-3 py-1 bg-black/40 text-cyber-cyan hover:bg-cyber-pink/20 transition font-bold">-</button>
                        <span class="px-4 font-mono text-white">${item.quantity}</span>
                        <button onclick="changeCartQty(${index}, 1)" class="px-3 py-1 bg-black/40 text-cyber-cyan hover:bg-cyber-pink/20 transition font-bold">+</button>
                    </div>

                    <!-- Subtotal del producto -->
                    <div class="text-right">
                        <span class="text-lg font-bold font-retro text-cyber-cyan">$${subtotalItem.toFixed(2)}</span>
                    </div>

                    <!-- Eliminar -->
                    <button onclick="removeCartItem(${index})" class="text-slate-400 hover:text-cyber-pink transition">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </div>
            </div>
        `;
    });

    const subtotal = shoppingCart.reduce((sum, item) => sum + (item.precio * item.quantity), 0);
    updateBillTotals(subtotal);
}

function changeCartQty(index, dir) {
    const item = shoppingCart[index];
    const newQty = item.quantity + dir;
    if (newQty <= 0) {
        removeCartItem(index);
    } else {
        item.quantity = newQty;
        localStorage.setItem('retropulse_cart', JSON.stringify(shoppingCart));
        renderCartPage();
        updateCartBadge();
    }
}

function removeCartItem(index) {
    const name = shoppingCart[index].nombre;
    shoppingCart.splice(index, 1);
    localStorage.setItem('retropulse_cart', JSON.stringify(shoppingCart));
    showNotificationToast(`Se removió ${name} del carrito.`, true);
    renderCartPage();
    updateCartBadge();
}

function updateBillTotals(subtotal) {
    const tax = subtotal * 0.16;
    const total = subtotal + tax;

    document.getElementById('cart-subtotal').innerText = `$${subtotal.toFixed(2)}`;
    document.getElementById('cart-tax').innerText = `$${tax.toFixed(2)}`;
    document.getElementById('cart-total').innerText = `$${total.toFixed(2)}`;
}

// Toast de notificación integrado
function showNotificationToast(message, isError = false) {
    const toast = document.getElementById('custom-toast');
    const toastMsg = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toast || !toastMsg || !toastIcon) return;

    toastMsg.innerText = message;
    if (isError) {
        toast.querySelector('div').className = "bg-cyber-card border-2 border-cyber-pink text-white px-6 py-3 rounded-lg shadow-[0_0_15px_rgba(255,0,127,0.4)] flex items-center gap-3";
        toastIcon.innerHTML = `<i class="fa-solid fa-triangle-exclamation text-cyber-pink"></i>`;
    } else {
        toast.querySelector('div').className = "bg-cyber-card border-2 border-cyber-cyan text-white px-6 py-3 rounded-lg shadow-[0_0_15px_rgba(0,240,255,0.4)] flex items-center gap-3";
        toastIcon.innerHTML = `<i class="fa-solid fa-circle-check text-cyber-cyan"></i>`;
    }

    toast.classList.remove('translate-y-20', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');

    setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
        toast.classList.remove('translate-y-0', 'opacity-100');
    }, 3000);
}