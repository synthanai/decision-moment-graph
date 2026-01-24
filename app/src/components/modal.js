/**
 * Modal Component
 */

export function showModal(modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Focus first input
    setTimeout(() => {
        const firstInput = modal.querySelector('input, textarea');
        if (firstInput) firstInput.focus();
    }, 100);
}

export function hideModal(modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
}
