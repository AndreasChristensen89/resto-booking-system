let isAnimating = false;

function switchMenu(id) {
    if (isAnimating) return;

    let elementId = id.toLowerCase();
    const targetID = document.getElementById(elementId);

    const menuItems = document.getElementsByClassName("menu-category");
    let currentlyDisplayedItem;

    for (let item of menuItems) {
        if (!item.classList.contains("d-none")) {
            currentlyDisplayedItem = item;
            item.classList.add("opacity-out");
        }
    }

    const handleFadeIn = () => {
        // Remove d-none from the target ID
        targetID.classList.remove('d-none');
        
        // Add opacity-in to the target ID
        targetID.classList.add("opacity-in");

        // Wait for animation to complete then remove opacity-in
        targetID.addEventListener("animationend", function handler() {
            targetID.classList.remove("opacity-in");
            targetID.removeEventListener("animationend", handler);
            isAnimating = false;
        });
    };

    isAnimating = true;

    if (currentlyDisplayedItem) {
        // Wait for animation to complete then add d-none and handle fade-in for new section
        currentlyDisplayedItem.addEventListener("animationend", function handler() {
            currentlyDisplayedItem.classList.add("d-none");
            currentlyDisplayedItem.classList.remove("opacity-out");
            currentlyDisplayedItem.removeEventListener("animationend", handler);
            
            // Start the 'opacity-in' animation
            handleFadeIn();
        });
    } else {
        // If there's no currently displayed item, just handle the fade-in
        handleFadeIn();
    }
}
