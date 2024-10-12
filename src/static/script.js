document.addEventListener("DOMContentLoaded", function() {
    let listingsContainer = document.querySelector(".listings-container");
    let isLoading = false;
    let page = 1;

    // Function to load more listings
    function loadMoreListings() {
        if (isLoading) return;

        isLoading = true;
        page += 1;

        fetch(`/load-more-listings?page=${page}`)
            .then(response => response.json())
            .then(data => {
                data.listings.forEach(item => {
                    let listingBox = document.createElement('div');
                    listingBox.className = 'listing-box';
                    listingBox.innerHTML = `<h3>${item.name}</h3><p>${item.description}</p>`;
                    listingsContainer.appendChild(listingBox);
                });
                isLoading = false;
            })
            .catch(() => {
                isLoading = false;
            });
    }

    // Listen to scroll event
    listingsContainer.addEventListener("scroll", function() {
        if (listingsContainer.scrollTop + listingsContainer.clientHeight >= listingsContainer.scrollHeight) {
            loadMoreListings();
        }
    });
});
