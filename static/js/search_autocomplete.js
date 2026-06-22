(function () {
    'use strict';

    const searchInput = document.getElementById('search-input');
    const autocompleteResults = document.getElementById('autocomplete-results');

    function performSearch() {
        var query = searchInput ? searchInput.value.trim() : '';
        if (query) {
            window.location.href = '/cameras/search/?q=' + encodeURIComponent(query);
        }
    }

    function showAutocomplete(results) {
        if (!autocompleteResults) return;
        autocompleteResults.innerHTML = '';
        if (!results || results.length === 0) {
            autocompleteResults.classList.remove('visible');
            return;
        }
        results.forEach(function (item) {
            var a = document.createElement('a');
            a.href = item.url;
            a.className = 'autocomplete-item';
            a.textContent = item.name + (item.year ? ' (' + item.year + ')' : '');
            autocompleteResults.appendChild(a);
        });
        autocompleteResults.classList.add('visible');
    }

    function hideAutocomplete() {
        if (autocompleteResults) {
            autocompleteResults.classList.remove('visible');
        }
    }

    var debounceTimer;
    function fetchAutocomplete() {
        var query = searchInput ? searchInput.value.trim() : '';
        if (query.length < 2) {
            hideAutocomplete();
            return;
        }
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function () {
            fetch('/api/search-autocomplete/?q=' + encodeURIComponent(query))
                .then(function (r) { return r.json(); })
                .then(showAutocomplete)
                .catch(function () { hideAutocomplete(); });
        }, 200);
    }

    if (searchInput) {
        searchInput.addEventListener('input', fetchAutocomplete);
        searchInput.addEventListener('focus', fetchAutocomplete);
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch();
            }
        });
    }

    document.addEventListener('click', function (e) {
        if (autocompleteResults && !searchInput.contains(e.target) && !autocompleteResults.contains(e.target)) {
            hideAutocomplete();
        }
    });

    window.performSearch = performSearch;
})();
