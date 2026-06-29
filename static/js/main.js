document.addEventListener('DOMContentLoaded', () => {
    initToasts();
    initDonationModal();
});

function initToasts() {
    document.querySelectorAll('.toast[data-auto-dismiss]').forEach(toast => {
        const delay = parseInt(toast.dataset.autoDismiss, 10) || 5000;
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity .3s';
            setTimeout(() => toast.remove(), 300);
        }, delay);
    });
}

function initDonationModal() {
    const modal = document.getElementById('donation-modal');
    const successModal = document.getElementById('success-modal');
    if (!modal) return;

    const form = document.getElementById('donation-form');
    const amountInput = document.getElementById('donation-amount');
    const needIdInput = document.getElementById('donation-need-id');
    const errorEl = document.getElementById('donation-error');

    document.querySelectorAll('.btn-donate').forEach(btn => {
        btn.addEventListener('click', () => {
            const needId = btn.dataset.needId;
            const needTitle = btn.dataset.needTitle;
            const communityName = btn.dataset.communityName;
            const remaining = parseFloat(btn.dataset.remaining);

            needIdInput.value = needId;
            document.getElementById('modal-subtitle').textContent =
                `Ayuda a ${communityName} con su necesidad de ${needTitle.split(' ').slice(-3).join(' ').toLowerCase()}.`;
            document.getElementById('modal-need-title').textContent = needTitle;
            document.getElementById('modal-remaining').textContent =
                '$' + remaining.toLocaleString('es-AR');
            amountInput.value = Math.min(10000, remaining);
            amountInput.max = remaining;
            errorEl.classList.add('hidden');
            modal.classList.remove('hidden');
        });
    });

    document.querySelectorAll('[data-close-modal]').forEach(el => {
        el.addEventListener('click', () => modal.classList.add('hidden'));
    });

    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            amountInput.value = btn.dataset.amount;
        });
    });

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorEl.classList.add('hidden');

        const needId = needIdInput.value;
        const url = window.DONATE_URL_TEMPLATE.replace('{id}', needId);
        const csrf = form.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrf,
                },
                body: new URLSearchParams({ amount: amountInput.value }),
            });

            const data = await response.json();

            if (!data.success) {
                errorEl.textContent = data.error || 'Error al procesar la donación.';
                errorEl.classList.remove('hidden');
                return;
            }

            modal.classList.add('hidden');
            showSuccessModal(data);
        } catch {
            errorEl.textContent = 'Error de conexión. Intentá de nuevo.';
            errorEl.classList.remove('hidden');
        }
    });

    document.querySelectorAll('[data-close-success]').forEach(el => {
        el.addEventListener('click', () => {
            successModal.classList.add('hidden');
            window.location.reload();
        });
    });
}

function showSuccessModal(data) {
    const successModal = document.getElementById('success-modal');
    document.getElementById('success-message').textContent =
        `Gracias por tu generosidad. Tu donación ayudará a ${data.community}.`;
    document.getElementById('success-amount').textContent =
        '$' + data.amount.toLocaleString('es-AR');
    document.getElementById('success-community').textContent = data.community;
    document.getElementById('success-need').textContent = data.need;
    document.getElementById('success-code').value = data.confirmation_code;
    successModal.classList.remove('hidden');
}

function showToast(message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast toast-show';
    toast.innerHTML = `<span class="toast-icon">✓</span><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 5000);
}
