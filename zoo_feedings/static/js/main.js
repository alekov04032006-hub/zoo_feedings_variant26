// Дополнительные сведения доступны с клавиатуры и меняют aria-expanded.
document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-toggle]');
    if (!button) return;
    const panel = document.getElementById(button.dataset.toggle);
    if (!panel) return;
    panel.hidden = !panel.hidden;
    button.setAttribute('aria-expanded', String(!panel.hidden));
    button.textContent = panel.hidden ? 'О вольере' : 'Скрыть сведения';
});
