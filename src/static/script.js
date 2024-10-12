document.addEventListener("DOMContentLoaded", function () {
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
                    listingBox.innerHTML = `<h3>${item.name}</h3><p>${item.description}</p><p>Price: $${item.price}</p>`;
                    listingsContainer.appendChild(listingBox);
                });
                isLoading = false;
            })
            .catch(() => {
                isLoading = false;
            });
    }

    // Listen to scroll event for infinite scrolling
    listingsContainer.addEventListener("scroll", function () {
        if (listingsContainer.scrollTop + listingsContainer.clientHeight >= listingsContainer.scrollHeight) {
            loadMoreListings();
        }
    });

    // For borrowing items (borrow_item.html functionality)
    let startDateInput = document.getElementById("start_date");
    let endDateInput = document.getElementById("end_date");
    let totalPriceInput = document.getElementById("total_price");

    if (startDateInput && endDateInput && totalPriceInput) {
        let pricePerDay = parseFloat(document.getElementById('price_per_day').textContent);  // Assuming price is rendered as text in HTML

        function calculateTotalPrice() {
            const startDate = new Date(startDateInput.value);
            const endDate = new Date(endDateInput.value);

            if (startDate && endDate && startDate < endDate) {
                const timeDifference = endDate.getTime() - startDate.getTime();
                const numDays = timeDifference / (1000 * 3600 * 24);  // Convert milliseconds to days
                const totalPrice = numDays * pricePerDay;
                totalPriceInput.value = totalPrice.toFixed(2);  // Set the total price in the input field
            }
        }

        // Attach event listeners to start and end date inputs for dynamic price calculation
        startDateInput.addEventListener("change", calculateTotalPrice);
        endDateInput.addEventListener("change", calculateTotalPrice);
    }
});