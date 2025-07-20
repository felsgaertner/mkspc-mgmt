function dateTimeSetNow(theId) {
    const now = new Date();
    const localNow = new Date(Date.UTC(
        now.getFullYear(), now.getMonth(), now.getDate(),
        now.getHours(), now.getMinutes()));
    dateFieldSet(theId, localNow);
    dateFieldSet(theId + '_day', localNow);
    dateFieldSet(theId + '_time', localNow);
}

function dateTimeReset(theId) {
    dateFieldSet(theId, null);
    dateFieldSet(theId + '_day', null);
    dateFieldSet(theId + '_time', null);
}

function dateFieldSet(theId, value = null) {
    const el = document.getElementById(theId);
    if (el) el.valueAsDate = value;
}

$(document).ready(function () {
    $('select').select2({
        width: '100%',
        placeholder: '–– nicht ausgewählt ––',
        allowClear: true,
        // minimumResultsForSearch: 7,
        // minimumInputLength: 1,
    });
});

$(document).on('select2:open', () => {
    document.querySelector('.select2-search__field').focus();
});
