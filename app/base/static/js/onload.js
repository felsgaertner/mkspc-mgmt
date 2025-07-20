document.querySelectorAll('.table[data-onclick]').forEach((tbl) => {
    tbl.classList.add('clickable');
    const callback = new Function(tbl.dataset.onclick);
    tbl.onclick = (event) => {
        const entry = event.target.closest('tbody>tr');
        if (entry) { callback.call(tbl, row=entry); }
    };
});
